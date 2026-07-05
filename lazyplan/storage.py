import json
from dataclasses import asdict
from pathlib import Path

from lazyplan.models import Project, Status

DATA_DIR = Path.home() / ".local" / "share" / "lazyplan"
DATA_FILE = DATA_DIR / "projects.json"


def load_projects() -> list[Project]:
    if not DATA_FILE.exists():
        return []
    try:
        data = json.loads(DATA_FILE.read_text())
        projects = []
        for p in data:
            p["status"] = Status(p.get("status", "cruda"))
            p.setdefault("stack", [])
            p.setdefault("links", [])
            p.setdefault("github_url", "")
            p.setdefault("folder_path", "")
            projects.append(Project(**p))
        return projects
    except Exception:
        return []


def save_projects(projects: list[Project]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(
            [asdict(p) for p in projects],
            indent=2,
            default=str,
        )
    )


def find_project(projects: list[Project], project_id: str) -> Project | None:
    return next((p for p in projects if p.id == project_id), None)


def upsert_project(projects: list[Project], project: Project) -> list[Project]:
    for i, p in enumerate(projects):
        if p.id == project.id:
            projects[i] = project
            return projects
    projects.insert(0, project)
    return projects


def delete_project(projects: list[Project], project_id: str) -> list[Project]:
    return [p for p in projects if p.id != project_id]
