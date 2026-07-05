from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Input, TextArea, Select, Label, Button, Static
from textual.binding import Binding
from textual.containers import Vertical, Horizontal, ScrollableContainer
from textual import on

from lazyplan.models import Project, Status

STACK_SUGGESTIONS = [
    # Backend
    "NestJS", "FastAPI", "Django", "Express", "Flask", "Hono", "Elysia",
    # Frontend
    "React", "Next.js", "Vue", "Nuxt", "Svelte", "Astro", "HTML/CSS",
    # Mobile
    "React Native", "Flutter",
    # DB
    "PostgreSQL", "MySQL", "SQLite", "MongoDB", "Redis",
    # DevOps
    "Docker", "GitHub Actions", "Nginx", "Caddy",
    # Lenguajes
    "Python", "TypeScript", "JavaScript", "Rust", "Go",
    # Otros
    "Textual", "Prisma", "GraphQL", "tRPC", "Tailwind",
]


class EditorScreen(Screen):
    """Screen para crear o editar un proyecto."""

    BINDINGS = [
        Binding("escape",   "cancel",        "Cancelar"),
        Binding("ctrl+s",   "save",          "Guardar"),
    ]

    def __init__(self, project: Project | None = None):
        super().__init__()
        self._project    = project
        self._is_editing = project is not None

    def compose(self) -> ComposeResult:
        p      = self._project
        title  = "Editar proyecto" if self._is_editing else "Nuevo proyecto"

        status_options = [(s.value.capitalize(), s) for s in Status]

        yield ScrollableContainer(
            Vertical(
                Static(f" 💤 LazyPlan  ›  {title}", id="editor-title"),

                Label("Título *", classes="form-label"),
                Input(
                    value=p.title if p else "",
                    placeholder="Nombre del proyecto",
                    id="input-title",
                ),

                Label("Descripción", classes="form-label"),
                TextArea(
                    text=p.description if p else "",
                    id="input-desc",
                ),

                Label("Stack (separado por comas)", classes="form-label"),
                Input(
                    value=p.stack_str if (p and p.stack) else "",
                    placeholder="Python, Textual, SQLite...",
                    id="input-stack",
                ),
                Static(
                    "Sugerencias: " + "  ·  ".join(STACK_SUGGESTIONS[:12]),
                    classes="form-hint",
                ),

                Label("Estado", classes="form-label"),
                Select(
                    options=status_options,
                    value=p.status if p else Status.CRUDA,
                    id="input-status",
                ),

                Label("Links (separados por comas)", classes="form-label"),
                Input(
                    value=", ".join(p.links) if (p and p.links) else "",
                    placeholder="https://..., https://...",
                    id="input-links",
                ),

                Static("", id="form-error"),

                Horizontal(
                    Button("Guardar  ctrl+s", variant="primary", id="btn-save"),
                    Button("Cancelar  esc",   variant="default",  id="btn-cancel"),
                    id="form-buttons",
                ),

                id="editor-form",
            ),
            id="editor-scroll",
        )
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#input-title", Input).focus()

    # ── Buttons ──────────────────────────────────────────────────────────────

    @on(Button.Pressed, "#btn-save")
    def on_save_clicked(self) -> None:
        self.action_save()

    @on(Button.Pressed, "#btn-cancel")
    def on_cancel_clicked(self) -> None:
        self.action_cancel()

    # ── Actions ──────────────────────────────────────────────────────────────

    def action_cancel(self) -> None:
        self.app.pop_screen()

    def action_save(self) -> None:
        title = self.query_one("#input-title", Input).value.strip()
        if not title:
            self.query_one("#form-error", Static).update(
                "[red]⚠  El título es obligatorio.[/red]"
            )
            self.query_one("#input-title", Input).focus()
            return

        desc   = self.query_one("#input-desc",   TextArea).text.strip()
        status = self.query_one("#input-status",  Select).value

        raw_stack = self.query_one("#input-stack", Input).value
        stack = [s.strip() for s in raw_stack.split(",") if s.strip()]

        raw_links = self.query_one("#input-links", Input).value
        links = [l.strip() for l in raw_links.split(",") if l.strip()]

        if self._is_editing and self._project:
            self._project.title       = title
            self._project.description = desc
            self._project.stack       = stack
            self._project.status      = status
            self._project.links       = links
            self._project.touch()
            project = self._project
        else:
            project = Project(
                title=title,
                description=desc,
                stack=stack,
                status=status,
                links=links,
            )

        self.app.save_project(project)
        self.app.pop_screen()
