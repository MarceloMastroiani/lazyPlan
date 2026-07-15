
from typing import TYPE_CHECKING, cast
from textual.screen import ModalScreen, Screen

if TYPE_CHECKING:
    from lazyplan.app import LazyPlanApp

class BaseScreen(Screen):

    # Esto es una propiedad para acceder al app como LazyPlanApp,
    # y así tener acceso a los métodos y propiedades específicos de la app.
    @property
    def lazyplan(self) -> "LazyPlanApp":
        return cast("LazyPlanApp", self.app)


class LazyPlanModalScreen(ModalScreen):
    @property
    def app(self) -> "LazyPlanApp":
        return cast("LazyPlanApp", super().app)
