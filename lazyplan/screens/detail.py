from textual.app import ComposeResult
from textual.widgets import Footer, Static, Label
from textual.binding import Binding
from textual.containers import Vertical, Horizontal, ScrollableContainer

from lazyplan.screens.base import BaseScreen

from lazyplan.models import Project


class DetailScreen(BaseScreen):
    """Vista de detalle de un proyecto (solo lectura)."""

    BINDINGS = [
        Binding("escape", "go_back",      "Volver"),
        Binding("e",      "edit_project", "Editar"),
        Binding("d",      "delete",       "Eliminar"),
        Binding("ctrl+g", "open_github",  "GitHub"),
    ]

    def __init__(self, project: Project):
        super().__init__()
        self._project = project

    def compose(self) -> ComposeResult:
        p = self._project
        created = p.created_at[:10].replace("-", "/") if p.created_at else "—"
        updated = p.updated_at[:10].replace("-", "/") if p.updated_at else "—"
        links   = "\n".join(f"• {link}" for link in p.links) if p.links else "—"

        yield ScrollableContainer(
            Vertical(
                # ── Bloque 1: Header ─────────────────────────────
                Horizontal(
                    Static(f"💤 lazyplan >> {p.title}", id="detail-title"),
                    Static(p.status_label, id="status-badge"),
                    id="detail-header",
                ),

                # ── Bloque 2: Descripción ─────────────────────────
                Vertical(
                    Static(" Descripción", classes="block-title"),
                    Static(p.description or "No especificado.", id="detail-desc"),
                    id="desc-block",
                ),

                # ── Bloque 3: Información + Metadatos ─────────────
                Horizontal(
                    Vertical(
                        Static(" Información", classes="block-title"),
                        Static("Stack", classes="field-label"),
                        Static(p.stack_str or "—", classes="field-value"),
                        Static("GitHub", classes="field-label"),
                        Static(p.github_url or "—", classes="field-value"),
                        id="col-info",
                        classes="detail-col",
                    ),
                    Vertical(
                        Static(" Metadatos", classes="block-title"),
                        Static("Estado",         classes="field-label"),
                        Static(p.status_label,   classes="field-value"),
                        Static("Carpeta",        classes="field-label"),
                        Static(p.folder_path or "—", classes="field-value"),
                        id="col-meta",
                        classes="detail-col",
                    ),
                    id="info-block",
                ),

                # ── Bloque 4: Links + Fechas ──────────────────────
                Horizontal(
                    Vertical(
                        Static(" Links", classes="block-title"),
                        Static(links or "—", id="detail-links"),
                        id="col-links",
                        classes="detail-col",
                    ),
                    Vertical(
                        Static(" Fechas", classes="block-title"),
                        Static("Creado",         classes="field-label"),
                        Static(created,          classes="field-value"),
                        Static("Editado",        classes="field-label"),
                        Static(updated,          classes="field-value"),
                        id="col-dates",
                        classes="detail-col",
                    ),
                    id="links-block",
                ),

                Static(
                    "[dim]e=editar  d=eliminar  esc=volver[/dim]",
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
        self.lazyplan.push_screen("editor", self._project)

    def action_delete(self) -> None:
        self.lazyplan.push_screen("confirm_delete", self._project)

    def action_open_github(self) -> None:
        self.lazyplan.push_screen("github", self._project)
