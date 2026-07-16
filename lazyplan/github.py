"""
Integración con GitHub CLI (gh) para LazyPlan.
Permite crear repos y hacer push inicial desde la TUI.
"""

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class GitHubResult:
    success: bool
    url: str = ""
    error: str = ""


def gh_available() -> bool:
    """Devuelve True si gh está instalado y autenticado."""
    try:
        result = subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True, text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def gh_username() -> str:
    """Devuelve el username de GitHub autenticado."""
    try:
        result = subprocess.run(
            ["gh", "api", "user", "--jq", ".login"],
            capture_output=True, text=True
        )
        return result.stdout.strip()
    except Exception:
        return ""


def create_github_repo(
    title: str,
    description: str = "",
    private: bool = True,
    folder_path: str = "",
) -> GitHubResult:
    """
    Crea un repo en GitHub y hace push inicial si hay carpeta.

    Args:
        title: Nombre del proyecto (se convierte a slug)
        description: Descripción del proyecto
        private: True = privado, False = público
        folder_path: Ruta local del proyecto para git init + push

    Returns:
        GitHubResult con success, url y error
    """
    slug = _to_slug(title)
    visibility = "--private" if private else "--public"

    # 1. Crear el repo en GitHub
    cmd = ["gh", "repo", "create", slug, visibility, "--confirm"]
    if description:
        cmd += ["--description", description[:255]]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return GitHubResult(
            success=False,
            error=result.stderr.strip() or "Error al crear el repositorio"
        )

    # URL del repo
    username = gh_username()
    repo_url = f"https://github.com/{username}/{slug}"

    # 2. Si hay carpeta local, inicializar git y hacer push
    if folder_path:
        folder = Path(folder_path)
        if folder.exists():
            push_result = _git_init_and_push(folder, repo_url, slug)
            if not push_result.success:
                # El repo se creó pero el push falló: no es fatal
                return GitHubResult(
                    success=True,
                    url=repo_url,
                    error=f"Repo creado pero push falló: {push_result.error}"
                )

    return GitHubResult(success=True, url=repo_url)


def _git_init_and_push(folder: Path, repo_url: str, slug: str) -> GitHubResult:
    """git init + add + commit + push en la carpeta dada."""
    commands = [
        ["git", "init"],
        ["git", "add", "."],
        ["git", "commit", "-m", "Initial commit – LazyPlan 💤"],
        ["git", "branch", "-M", "main"],
        ["git", "remote", "add", "origin", f"{repo_url}.git"],
        ["git", "push", "-u", "origin", "main"],
    ]

    for cmd in commands:
        result = subprocess.run(
            cmd, cwd=str(folder), capture_output=True, text=True
        )
        if result.returncode != 0:
            return GitHubResult(
                success=False,
                error=f"Falló '{' '.join(cmd)}': {result.stderr.strip()}"
            )

    return GitHubResult(success=True, url=repo_url)


def _to_slug(title: str) -> str:
    """Convierte un título a slug válido para GitHub."""
    import re
    slug = title.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "mi-proyecto"
