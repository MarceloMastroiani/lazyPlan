# 💤 LazyPlan

TUI (interfaz de terminal) para capturar y gestionar ideas de proyectos, sin salir de la consola. Anotá una idea en 5 segundos, hacé seguimiento de su estado, y creá el repo en GitHub cuando estés listo para arrancar — todo desde el teclado.

<!--![status](https://img.shields.io/badge/status-en%20desarrollo-yellow)
![python](https://img.shields.io/badge/python-3.11%2B-blue)
![textual](https://img.shields.io/badge/built%20with-Textual-8839ef)-->

---

## ✨ Características

- **Captura rápida de ideas** desde la TUI o directo desde la terminal (`lazyplan new`).
- **Estados de proyecto**: 🟡 Cruda · 🟢 Activa · ⚪ Pausada · 🔴 Descartada.
- **Búsqueda y filtros** en tiempo real por título, descripción o stack.
- **Vista de detalle** con toda la info del proyecto.
- **Editor integrado** para crear y modificar proyectos sin salir de la app.
- **Integración con GitHub CLI (`gh`)**: creá un repositorio (público o privado) directamente desde la TUI, sin abrir el navegador.
- **Persistencia local** en JSON, sin bases de datos ni servicios externos.
- Tema oscuro propio (`onyx-violet`) 🎨

---

## 📦 Requisitos

- Python **3.11** o superior
- [GitHub CLI (`gh`)](https://cli.github.com/) instalado y autenticado — **solo si** querés usar la creación de repos desde la app (`ctrl+g`). El resto de LazyPlan funciona sin `gh`.

---

## 🚀 Instalación

### Con pipx (recomendado)

```bash
pipx install lazyplan
```

### Con pip

```bash
pip install lazyplan
```

### Desde el código fuente

```bash
git clone https://github.com/tu-usuario/lazyplan.git
cd lazyplan
pip install -e .
```

---

## 🕹️ Uso

### Abrir la TUI

```bash
lazyplan
```

### Crear un proyecto sin abrir la TUI

```bash
lazyplan new -t "Mi idea genial" -s "python,textual" -d "Una app de terminal" --status cruda
```

| Opción | Descripción |
|---|---|
| `-t`, `--title` | Título del proyecto **(obligatorio)** |
| `-s`, `--stack` | Tecnologías, separadas por coma |
| `-d`, `--desc` | Descripción breve |
| `--status` | Estado inicial: `cruda`, `activa`, `pausada`, `descartada` (default: `cruda`) |

### Listar proyectos desde la terminal

```bash
lazyplan ls
```

---

## ⌨️ Atajos de teclado (dentro de la TUI)

**Pantalla principal**

| Tecla | Acción |
|---|---|
| `n` | Nuevo proyecto |
| `enter` | Ver detalle |
| `e` | Editar proyecto |
| `d` | Eliminar proyecto |
| `j` / `k` | Mover cursor abajo / arriba |
| `ctrl+f` | Buscar |
| `esc` | Limpiar búsqueda |
| `q` | Salir |

**Detalle del proyecto**

| Tecla | Acción |
|---|---|
| `e` | Editar |
| `d` | Eliminar |
| `ctrl+g` | Crear repositorio en GitHub |
| `esc` | Volver |

**Editor**

| Tecla | Acción |
|---|---|
| `ctrl+s` | Guardar |
| `esc` | Cancelar |

---

## 💾 Dónde se guardan los datos

LazyPlan guarda todo en un archivo JSON local, sin necesidad de conexión a internet ni servicios externos:

```
~/.local/share/lazyplan/projects.json
```

---

## 🏗️ Estructura del proyecto

```
lazyplan/
├── lazyplan/
│   ├── app.py              # App principal de Textual
│   ├── cli.py               # Entry point y comandos (typer)
│   ├── models.py             # Modelo Project / Status
│   ├── storage.py            # Persistencia en JSON
│   ├── github.py             # Integración con GitHub CLI
│   ├── lazyplan.tcss          # Estilos (Textual CSS)
│   └── screens/
│       ├── main.py           # Listado principal
│       ├── detail.py          # Vista de detalle
│       ├── editor.py          # Crear/editar proyecto
│       ├── confirm_delete.py   # Confirmación de borrado
│       └── github_screen.py    # Modal de creación de repo
└── pyproject.toml
```

---

## 🛠️ Desarrollo

Cloná el repo e instalá las dependencias de desarrollo (incluye herramientas de build y empaquetado):

```bash
git clone https://github.com/tu-usuario/lazyplan.git
cd lazyplan
pip install -e ".[dev]"
```

Correr la app en modo desarrollo:

```bash
python -m lazyplan.cli
```

### Generar el paquete

```bash
python -m build
```

### Publicar en PyPI

```bash
twine upload dist/*
```

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Si encontrás un bug o tenés una idea:

1. Abrí un issue describiendo el problema o la propuesta.
2. Forkeá el repo y creá una rama (`git checkout -b feature/mi-mejora`).
3. Hacé tus cambios y abrí un Pull Request.

---

## 📄 Licencia

Este proyecto no tiene licencia definida todavía. Si pensás distribuirlo o aceptar contribuciones externas, considerá agregar una (por ejemplo, [MIT](https://choosealicense.com/licenses/mit/)).

---

## ✍️ Autor

**Marcelo Mastroiani** — mastroianimarcelo04@gmail.com
