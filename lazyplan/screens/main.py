from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import DataTable, Input, Footer, Label, Static
from textual.binding import Binding
from textual.containers import Vertical, Horizontal
from textual import on

from lazyplan.models import Project, Status


class MainScreen(Screen):
    """Pantalla principal: lista de proyectos."""

    BINDINGS = [
        Binding("n",       "new_project",    "Nuevo"),
        Binding("enter",   "open_detail",    "Ver detalle"),
        Binding("e",       "edit_project",   "Editar"),
        Binding("d",       "delete_project", "Eliminar"),
        Binding("j",       "move_down",      "Abajo",  show=False),
        Binding("k",       "move_up",        "Arriba", show=False),
        Binding("ctrl+f",  "focus_search",   "Buscar"),
        Binding("escape",  "clear_search",   "Limpiar", show=False),
        Binding("q",       "quit_app",       "Salir"),
    ]

    def __init__(self, projects: list[Project]):
        super().__init__()
        self._all_projects  = projects
        self._filtered      = projects[:]
        self._active_filter = "all"

    # ── Layout ───────────────────────────────────────────────────────────────

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static(" 💤 LazyPlan", id="app-title"),
            Horizontal(
                Input(placeholder="  🔍  Buscar proyecto... (ctrl+f)", id="search"),
                id="search-bar",
            ),
            Horizontal(
                Label("[b]Filtro:[/b]", id="filter-label"),
                Static("[u]Todos[/u]",     id="f-all",        classes="filter-btn active"),
                Static("🟡 Cruda",         id="f-cruda",      classes="filter-btn"),
                Static("🟢 Activa",        id="f-activa",     classes="filter-btn"),
                Static("⚪ Pausada",       id="f-pausada",    classes="filter-btn"),
                Static("🔴 Descartada",   id="f-descartada", classes="filter-btn"),
                id="filter-bar",
            ),
            DataTable(id="project-table", cursor_type="row", zebra_stripes=True),
            Static(self._status_bar(), id="status-bar"),
            id="main-layout",
        )
        yield Footer()

    def on_mount(self) -> None:
        self._setup_table()
        self._populate_table()

    def _setup_table(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("ID", "Título", "Stack", "Estado", "Creado")

    def _populate_table(self) -> None:
        table = self.query_one(DataTable)
        table.clear()
        for p in self._filtered:
            created = p.created_at[:10] if p.created_at else "—"
            table.add_row(
                p.id,
                p.title,
                p.stack_str[:40] + ("…" if len(p.stack_str) > 40 else ""),
                p.status_label,
                created,
                key=p.id,
            )
        self.query_one("#status-bar", Static).update(self._status_bar())

    def _status_bar(self) -> str:
        total     = len(self._all_projects)
        showing   = len(self._filtered)
        activos   = sum(1 for p in self._all_projects if p.status.value == "activa")
        return (
            f" {showing}/{total} proyectos  ·  "
            f"🟢 {activos} activos  ·  "
            f"[dim]n=nuevo  enter=detalle  e=editar  d=eliminar  q=salir[/dim]"
        )

    # ── Filtro y búsqueda ────────────────────────────────────────────────────

    def _apply_filters(self, query: str = "") -> None:
        q = query.lower().strip()
        result = self._all_projects

        if self._active_filter != "all":
            result = [p for p in result if p.status.value == self._active_filter]

        if q:
            result = [
                p for p in result
                if q in p.title.lower()
                or q in p.description.lower()
                or q in p.stack_str.lower()
            ]

        self._filtered = result
        self._populate_table()

    @on(Input.Changed, "#search")
    def on_search_changed(self, event: Input.Changed) -> None:
        self._apply_filters(event.value)

    def on_static_click(self, event) -> None:
        """Maneja clicks en los botones de filtro."""
        widget_id = event.widget.id
        if not widget_id or not widget_id.startswith("f-"):
            return

        # Actualizar clases activas
        for btn in self.query(".filter-btn"):
            btn.remove_class("active")
        event.widget.add_class("active")

        self._active_filter = widget_id.replace("f-", "")
        search_text = self.query_one("#search", Input).value
        self._apply_filters(search_text)

    # ── Helpers ──────────────────────────────────────────────────────────────

    def _selected_project(self) -> Project | None:
        table = self.query_one(DataTable)
        if not table.row_count:
            return None
        row_key = table.cursor_row
        try:
            row_data = table.get_row_at(row_key)
            project_id = row_data[0]
            return next((p for p in self._filtered if p.id == project_id), None)
        except Exception:
            return None

    def refresh_projects(self, projects: list[Project]) -> None:
        """Llamado desde la App después de guardar cambios."""
        self._all_projects = projects
        self._apply_filters(self.query_one("#search", Input).value)

    # ── Actions ──────────────────────────────────────────────────────────────

    def action_move_down(self) -> None:
        self.query_one(DataTable).action_scroll_down()

    def action_move_up(self) -> None:
        self.query_one(DataTable).action_scroll_up()

    def action_focus_search(self) -> None:
        self.query_one("#search", Input).focus()

    def action_clear_search(self) -> None:
        search = self.query_one("#search", Input)
        if search.value:
            search.value = ""
        else:
            self.query_one(DataTable).focus()

    def action_new_project(self) -> None:
        self.app.push_screen("editor")

    def action_open_detail(self) -> None:
        project = self._selected_project()
        if project:
            self.app.push_screen("detail", project)

    def action_edit_project(self) -> None:
        project = self._selected_project()
        if project:
            self.app.push_screen("editor", project)

    def action_delete_project(self) -> None:
        project = self._selected_project()
        if project:
            self.app.push_screen("confirm_delete", project)

    def action_quit_app(self) -> None:
        self.app.exit()

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        project = self._selected_project()
        if project:
            self.app.push_screen("detail", project)
