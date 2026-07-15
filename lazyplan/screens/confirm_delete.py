from textual.app import ComposeResult
from textual.widgets import Button, Static, Label
from textual.containers import Vertical, Horizontal
from textual.binding import Binding
from textual import on

from lazyplan.screens.base import LazyPlanModalScreen

from lazyplan.models import Project


class ConfirmDeleteScreen(LazyPlanModalScreen):
    """Modal de confirmación para eliminar un proyecto."""

    BINDINGS = [
        Binding("escape", "cancel", "Cancelar"),
        Binding("y",      "confirm", "Confirmar", show=False),
    ]

    def __init__(self, project: Project):
        super().__init__()
        self._project = project

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("⚠  Eliminar proyecto", id="confirm-title"),
            Label(
                f'¿Seguro que querés eliminar\n[b]"{self._project.title}"[/b]?\n\n'
                "Esta acción no se puede deshacer.",
                id="confirm-body",
            ),
            Horizontal(
                Button("Sí, eliminar  (y)", variant="error",   id="btn-confirm"),
                Button("Cancelar  (esc)",   variant="default",  id="btn-cancel"),
                id="confirm-buttons",
            ),
            id="confirm-dialog",
        )

    @on(Button.Pressed, "#btn-confirm")
    def on_confirm(self) -> None:
        self.action_confirm()

    @on(Button.Pressed, "#btn-cancel")
    def on_cancel(self) -> None:
        self.action_cancel()

    def action_confirm(self) -> None:
        self.app.delete_project(self._project.id)
        self.app.pop_screen()

    def action_cancel(self) -> None:
        self.app.pop_screen()
