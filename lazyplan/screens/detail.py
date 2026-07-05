from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Static, Label
from textual.binding import Binding
from textual.containers import Vertical, Horizontal, ScrollableContainer

from lazyplan.models import Project


class DetailScreen(Screen):
    """Vista de detalle de un proyecto (solo lectura)."""

    BINDINGS = [
        Binding("escape", "go_back",      "Volver"),
        Binding("e",      "edit_project", "Editar"),
        Binding("d",      "delete",       "Eliminar"),
    ]

    def __init__(self, project: Project):
        super().__init__()
        self._project = project

    def compose(self) -> ComposeResult:
        p = self._project
        created = p.created_at[:16].replace("T", " ") if p.created_at else "—"
        updated = p.updated_at[:16].replace("T", " ") if p.updated_at else "—"

        yield ScrollableContainer(
            Vertical(
                Static(f" 💤 LazyPlan  ›  {p.title}", id="detail-title"),
                Horizontal(
                    Static(p.status_label, id="status-badge"),
                    Static(f"ID: {p.id}", id="id-badge"),
                    id="badges",
                ),
                self._field("📝  Descripción", p.description or "Sin descripción."),
                self._field("🔧  Stack",        p.stack_str),
                self._field("🔗  Links",        "\n".join(p.links) if p.links else "—"),
                self._field("🐙  GitHub",       p.github_url or "—"),
                self._field("📁  Carpeta",      p.folder_path or "—"),
                Horizontal(
                    self._field("📅  Creado",   created, small=True),
                    self._field("✏️  Editado",  updated, small=True),
                    id="meta-row",
                ),
                Static(
                    "[dim]e=editar  d=eliminar  escape=volver[/dim]",
                    id="detail-hint",
                ),
                id="detail-content",
            ),
            id="detail-scroll",
        )
        yield Footer()

    def _field(self, label: str, value: str, small: bool = False) -> Vertical:
        cls = "field-small" if small else "field"
        return Vertical(
            Label(label, classes="field-label"),
            Static(value or "—", classes="field-value"),
            classes=cls,
        )

    # ── Actions ──────────────────────────────────────────────────────────────

    def action_go_back(self) -> None:
        self.app.pop_screen()

    def action_edit_project(self) -> None:
        self.app.pop_screen()
        self.app.push_screen("editor", self._project)

    def action_delete(self) -> None:
        self.app.push_screen("confirm_delete", self._project)
