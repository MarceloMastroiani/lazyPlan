from textual.app import App

from lazyplan.models import Project
from lazyplan.storage import load_projects, save_projects, upsert_project, delete_project
from lazyplan.screens.main import MainScreen
from lazyplan.screens.detail import DetailScreen
from lazyplan.screens.editor import EditorScreen
from lazyplan.screens.confirm_delete import ConfirmDeleteScreen


class LazyPlanApp(App):
    """TUI para capturar y gestionar ideas de proyectos."""

    CSS_PATH = "lazyplan.css"
    TITLE    = "LazyPlan"

    SCREENS = {
        "main":           MainScreen,
        "detail":         DetailScreen,
        "editor":         EditorScreen,
        "confirm_delete": ConfirmDeleteScreen,
    }

    def __init__(self):
        super().__init__()
        self._projects = load_projects()

    def on_mount(self) -> None:
        self.push_screen(MainScreen(self._projects))

    # ── Screen helpers ────────────────────────────────────────────────────────

    def push_screen(self, screen, *args, **kwargs):
        """Override para pasar argumentos a las screens por nombre."""
        if isinstance(screen, str):
            name = screen
            if name == "detail" and args:
                screen = DetailScreen(args[0])
            elif name == "editor":
                screen = EditorScreen(args[0] if args else None)
            elif name == "confirm_delete" and args:
                screen = ConfirmDeleteScreen(args[0])
            else:
                screen = self.SCREENS[name]()
        return super().push_screen(screen, **kwargs)

    # ── Data operations (llamadas desde cualquier screen) ────────────────────

    def save_project(self, project: Project) -> None:
        self._projects = upsert_project(self._projects, project)
        save_projects(self._projects)
        self._refresh_main()

    def delete_project(self, project_id: str) -> None:
        self._projects = delete_project(self._projects, project_id)
        save_projects(self._projects)
        self._refresh_main()

    def _refresh_main(self) -> None:
        """Actualiza la lista en MainScreen si está en el stack."""
        for screen in self.screen_stack:
            if isinstance(screen, MainScreen):
                screen.refresh_projects(self._projects)
                break


def run():
    LazyPlanApp().run()


if __name__ == "__main__":
    run()
