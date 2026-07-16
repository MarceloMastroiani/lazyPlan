"""
Screen modal para crear un repositorio GitHub desde la TUI.
Se abre desde la vista de detalle con ctrl+g.
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, Horizontal
from textual.widgets import Button, Label, Static, Switch
from textual import on, work

from lazyplan.screens.base import LazyPlanModalScreen
from lazyplan.models import Project
from lazyplan import github


class GithubScreen(LazyPlanModalScreen):
    """Modal para crear un repo en GitHub."""

    BINDINGS = [
        Binding("escape", "cancel", "Cancelar"),
    ]

    def __init__(self, project: Project):
        super().__init__()
        self._project = project
        self._gh_available = github.gh_available()

    def compose(self) -> ComposeResult:
        p = self._project
        available = self._gh_available

        if not available:
            yield Vertical(
                Static("🐙  GitHub CLI no disponible", id="gh-title"),
                Static(
                    "gh no está instalado o no estás autenticado.\n\n"
                    "Instalá gh con:\n"
                    "  sudo apt install gh  (Debian/Ubuntu)\n"
                    "  brew install gh      (Mac)\n\n"
                    "Luego autenticáte con:\n"
                    "  gh auth login",
                    id="gh-error-body",
                ),
                Button("Cerrar  esc", variant="default", id="btn-cancel"),
                id="gh-dialog",
            )
            return

        yield Vertical(
            Static("🐙  Crear repositorio en GitHub", id="gh-title"),
            Label(f"Proyecto: [b]{p.title}[/b]", id="gh-project-label"),
            Static(
                f"Se creará: [b]github.com/…/{self._slug()}[/b]",
                id="gh-slug-label",
            ),
            Horizontal(
                Label("Repositorio privado", id="gh-private-label"),
                Switch(value=True, id="gh-private-switch"),
                id="gh-private-row",
            ),
            Static("", id="gh-status"),
            Horizontal(
                Button("Crear repo  ↵", variant="primary", id="btn-create"),
                Button("Cancelar  esc", variant="default", id="btn-cancel"),
                id="gh-buttons",
            ),
            id="gh-dialog",
        )

    def _slug(self) -> str:
        return github._to_slug(self._project.title)

    # ── Events ───────────────────────────────────────────────────────────────

    @on(Button.Pressed, "#btn-cancel")
    def on_cancel(self) -> None:
        self.action_cancel()

    @on(Button.Pressed, "#btn-create")
    def on_create(self) -> None:
        # Leemos el Switch acá porque este handler SÍ corre en el hilo principal.
        private_switch = self.query_one("#gh-private-switch", Switch)
        self._start_create(private_switch.value)

    def action_cancel(self) -> None:
        self.app.pop_screen()

    # ── Worker (corre en background para no bloquear la TUI) ─────────────────

    @work(thread=True)
    def _start_create(self, private: bool) -> None:
        """Crea el repo en un thread separado para no freezar la UI."""
        # Deshabilitar botones mientras trabaja
        self.app.call_from_thread(self._set_ui_loading, True)

        result = github.create_github_repo(
            title=self._project.title,
            description=self._project.description[:255],
            private=private,
            folder_path=self._project.folder_path,
        )

        self.app.call_from_thread(self._on_result, result)

    def _set_ui_loading(self, loading: bool) -> None:
        try:
            btn = self.query_one("#btn-create", Button)
            btn.disabled = loading
            status = self.query_one("#gh-status", Static)
            if loading:
                status.update("[yellow]⏳ Creando repositorio...[/yellow]")
        except Exception:
            pass

    def _on_result(self, result: "github.GitHubResult") -> None:
        try:
            status = self.query_one("#gh-status", Static)
            if result.success:
                status.update(f"[green]✅ Repo creado: {result.url}[/green]")
                # Guardar URL en el proyecto
                self._project.github_url = result.url
                self._project.touch()
                self.app.save_project(self._project)
                # Cerrar después de 2 segundos
                self.set_timer(2, self.app.pop_screen)
            else:
                status.update(f"[red]❌ Error: {result.error}[/red]")
                btn = self.query_one("#btn-create", Button)
                btn.disabled = False
        except Exception:
            pass
