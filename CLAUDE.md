# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

- **Install dependencies**: `pip install -r requirements.txt`
- **Run the application**: `python app.py` (starts Flask on `http://127.0.0.1:5001/` in debug mode)
- **Run the test suite**: `pytest` (uses `pytest` and `pytest-flask`)
- **Run a single test**: `pytest path/to/test_file.py::test_name`
- **Lint / format** (if a linter is added later): `flake8 .` or `black .`
- **Database migration placeholder**: future steps may add `flask db` commands once a migration tool is introduced.

## High‑Level Architecture & Structure

- **Entry point (`app.py`)** – creates the Flask app, registers routes, and runs the server. Routes are defined with `@app.route` decorators and currently render placeholder templates or return simple strings.
- **Templates (`templates/`)** – Jinja2 HTML files. `base.html` provides the common layout (navbar, footer, CSS/JS includes). Other pages (`landing.html`, `login.html`, `register.html`, etc.) extend `base.html` via `{% extends "base.html" %}` and fill the `{% block content %}` section.
- **Static assets (`static/`)** – `css/style.css` defines design tokens and component styles. `js/main.js` is a stub for future client‑side logic (e.g., form validation, charts). The modal for “See how it works” is also styled here.
- **Database layer (`database/db.py`)** – Currently a stub with comments describing required functions (`get_db()`, `init_db()`, `seed_db()`). Intended to hold SQLite connection logic and schema creation for users and expenses.
- **Routing Overview**
  - `/` → `landing.html`
  - `/register` → `register.html`
  - `/login` → `login.html`
  - `/logout`, `/profile`, `/expenses/*` – placeholders that will later interact with the database.
- **Testing** – The project uses `pytest` with the `pytest-flask` plugin. Tests should be placed under a `tests/` directory and can use the `client` fixture provided by `pytest-flask` to make requests against the Flask app.
- **Future Extension Points** – Add authentication, expense CRUD operations, database migrations, and richer client‑side interactivity. The modular layout (separate `app.py`, `database/`, `templates/`, `static/`) makes it straightforward to expand each concern.

## Project Structure (summarized)
```
expense-tracker/
├─ app.py                # Flask app entry point & route definitions
├─ requirements.txt      # Python dependencies
├─ database/
│   └─ db.py             # SQLite connection placeholder
├─ static/
│   ├─ css/style.css     # Global stylesheet & design tokens
│   └─ js/main.js        # Stub for JavaScript code
├─ templates/
│   ├─ base.html         # Master layout (navbar, footer, blocks)
│   ├─ landing.html      # Home page (includes modal for video)
│   ├─ login.html
│   ├─ register.html
│   └─ … (other pages)
└─ CLAUDE.md            # This guidance file
```

Use these commands and the architectural overview to quickly get up to speed when developing or extending the expense‑tracker application.
