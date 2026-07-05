# 💤 LazyPlan

TUI para capturar y gestionar ideas de proyectos. Estilo lazygit/lazydocker.

## Instalación

```bash
# Clonar y entrar al proyecto
git clone https://github.com/MarceloMastroiani/lazyplan
cd lazyplan

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate

# Instalar
pip install -e .
```

## Uso

```bash
# Abrir la TUI
lazyplan

# Captura rápida (sin abrir la TUI)
lazyplan new -t "Mi idea" -s "Python, Textual" -d "Descripción breve"

# Listar proyectos en terminal
lazyplan ls
```

## Atajos en la TUI

| Tecla     | Acción            |
|-----------|-------------------|
| `n`       | Nuevo proyecto    |
| `enter`   | Ver detalle       |
| `e`       | Editar            |
| `d`       | Eliminar          |
| `j / k`   | Navegar           |
| `ctrl+f`  | Buscar            |
| `q`       | Salir             |
| `ctrl+s`  | Guardar (editor)  |
| `esc`     | Volver / cancelar |

## Stack

- Python 3.11+
- [Textual](https://textual.textualize.io/) — TUI framework
- [Typer](https://typer.tiangolo.com/) — CLI
- JSON — Persistencia local en `~/.local/share/lazyplan/`
