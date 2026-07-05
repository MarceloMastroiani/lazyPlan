import typer
from lazyplan.storage import load_projects, save_projects, upsert_project
from lazyplan.models import Project, Status

app = typer.Typer(
    name="lazyplan",
    help="TUI para capturar y gestionar ideas de proyectos.",
    no_args_is_help=False,
)


@app.callback(invoke_without_command=True)
def default(ctx: typer.Context):
    """Abre la TUI si no se pasa ningún subcomando."""
    if ctx.invoked_subcommand is None:
        from lazyplan.app import LazyPlanApp
        LazyPlanApp().run()


@app.command()
def new(
    title:  str = typer.Option(..., "-t", "--title",  help="Título del proyecto"),
    stack:  str = typer.Option("",  "-s", "--stack",  help="Stack separado por comas"),
    desc:   str = typer.Option("",  "-d", "--desc",   help="Descripción"),
    status: str = typer.Option("cruda", "--status",   help="Estado inicial"),
):
    """Guarda un proyecto rápido sin abrir la TUI."""
    stack_list = [s.strip() for s in stack.split(",") if s.strip()]
    try:
        st = Status(status)
    except ValueError:
        st = Status.CRUDA

    project = Project(title=title, description=desc, stack=stack_list, status=st)
    projects = load_projects()
    projects = upsert_project(projects, project)
    save_projects(projects)
    typer.echo(f"✅  Proyecto '{title}' guardado  [ID: {project.id}]")


@app.command()
def ls():
    """Lista los proyectos en la terminal (sin TUI)."""
    projects = load_projects()
    if not projects:
        typer.echo("Sin proyectos todavía. Usá: lazyplan new -t 'Mi idea'")
        return
    for p in projects:
        typer.echo(f"  {p.id}  {p.status_label}  {p.title}  [{p.stack_str}]")


if __name__ == "__main__":
    app()
