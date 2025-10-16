# Copilot Instructions for Near-Here

## Project Overview
Near-Here is a Python-based application for discovering sustainable locations. The codebase is organized with clear separation between data, logic, and assets. Key files include `main.py` (entry point), `location.py` (location logic), and the `llocs_sostenibles/` directory (data and utilities).

## Architecture & Data Flow
- **Entry Point:** `main.py` orchestrates the app, likely loading data from JSON files and delegating to logic modules.
- **Location Logic:** `location.py` contains core functions/classes for handling location data.
- **Data Files:** JSON files (`llocs_sostenibles.json`, files in `src/`) store location and UI data. Always validate file paths and data formats.
- **Assets:** All images, fonts, and UI resources are under `assets/` and `src/info/`.
- **Utilities:** The `llocs_sostenibles/` directory contains scripts for data manipulation (e.g., `add_photos.py`, `classe.py`).

## Developer Workflows
- **Run the App:** Use `python main.py` from the project root.
- **Dependencies:** Install with `pip install -r requirements.txt`.
- **Data Updates:** Scripts in `llocs_sostenibles/` are used to update or process location data. Run them directly as needed.
- **No formal test suite detected.** If adding tests, place them in a dedicated `tests/` directory and follow project import patterns.

## Project Conventions
- **File Naming:** Use lowercase with underscores for Python files. JSON files are camel case or lowercase.
- **Data Access:** Always use provided utility scripts for modifying location data to ensure consistency.
- **Asset Usage:** Reference assets using relative paths from the project root.
- **No framework detected:** Code is plain Python; avoid introducing frameworks unless discussed.

## Integration Points
- **External Dependencies:** All dependencies should be listed in `requirements.txt`.
- **Data Format:** Location data is stored in JSON; ensure compatibility when updating or adding new data files.
- **Cross-Component Communication:** Data flows from JSON files to logic modules, then to the main app. Keep interfaces simple and document any new data structures in the README.

## Examples
- To add a new location, update `llocs_sostenibles.json` and use `llocs_sostenibles/add_photos.py` if photos are needed.
- To change UI assets, update files in `assets/` or `src/info/` and reference them in code using relative paths.

## Key Files & Directories
- `main.py`: Application entry point
- `location.py`: Location logic
- `llocs_sostenibles/`: Data utilities and scripts
- `llocs_sostenibles.json`: Main data file
- `assets/`, `src/`: UI and data assets

---
_If any conventions or workflows are unclear, please ask for clarification or provide feedback to improve these instructions._
