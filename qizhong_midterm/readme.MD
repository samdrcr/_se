# CataL1st OS (Student Hub)

**CataL1st OS** is a terminal-themed, edge-hosted student operating system and self-reminder application. Engineered to run entirely on the edge utilizing Cloudflare Workers and Pyodide, this single-file application seamlessly integrates a Python-based FastAPI backend with a reactive Vue.js 3 and Tailwind CSS frontend.

## Features

- **SYS_DIRECTIVES (Task Management):** Create, track, and complete assignments or tasks with assigned due dates. The system automatically sorts by date and highlights critical priority items.
- **FOCUS_PROTOCOL (Pomodoro Timer):** A built-in 25-minute focus timer that automatically logs "Compute Time" (study minutes) upon session completion.
- **FINANCE_LOG (Expense Tracker):** Log daily expenses to systematically track total resource expenditure in NT$.
- **SCRATCHPAD (Quick Notes):** A persistent text area for recording quick thoughts and temporary data, automatically saved to the active session.
- **Edge-Native Architecture:** Deployed via WebAssembly to Cloudflare's global edge network to ensure ultra-low latency.
- **Local State Management:** As edge workers remain stateless across cold starts, the operating system features a robust JSON-based Export and Import mechanism to back up and restore the entire workspace state seamlessly.

## Technical Stack

- **Backend:** Python 3.11+, FastAPI (v0.99.1), Pydantic (v1)
- **Frontend:** Vue.js 3 (CDN), Tailwind CSS (CDN), FontAwesome
- **Infrastructure:** Cloudflare Workers, Pyodide, `pywrangler` package manager

> **Dependency Note:** This project explicitly caps FastAPI (`<0.100.0`) and Pydantic (`<2.0.0`). Newer versions utilize heavily compiled Rust cores (such as `pydantic-core` and OpenTelemetry) which exceed Cloudflare's strict 1000ms CPU startup limit on the free tier.

## Prerequisites

Before initiating deployment, ensure the following dependencies are installed on the host system:

1.  **Node.js & npm** (Required for the base Wrangler CLI)
2.  **uv** (An optimized Python package installer)

Execute the following commands to install `uv` and the Python workers toolkit:

```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
source $HOME/.local/bin/env
uv tool install workers-py
```

## Project Structure

```text
catal1st-os/
├── pyproject.toml      # Python dependencies and project metadata
├── wrangler.toml       # Cloudflare worker configuration
└── src/
    └── main.py         # The core application logic (FastAPI + Vue Frontend)
```

## Local Development

1. **Initialize the environment files:**
   Ensure `wrangler.toml` and `pyproject.toml` are correctly configured in the root directory.

2. **Start the local edge simulator:**

   ```bash
   pywrangler dev
   ```

   _Note: This command utilizes `uv` to bundle FastAPI into a `.venv-workers` environment and initializes a local Pyodide instance._

3. **Access the Interface:**
   Once the terminal outputs `Ready on http://localhost:8787`, press `b` in the terminal to open the application in the default web browser.

## Deployment

To push the operating system live to the Cloudflare global network, execute:

```bash
pywrangler deploy
```

Upon successful deployment, Cloudflare will provision a permanent `.workers.dev` URL (e.g., `https://self-reminder-app.sam-catal1st.workers.dev/`).

## Data Persistence

Cloudflare Workers operate on a serverless architecture and spin down following periods of inactivity. Because this iteration of CataL1st OS utilizes an in-memory database (`db = {}`), **all data will reset when the worker enters a sleep state.**

**Standard Operating Procedure for Data Persistence:**

1. Click **EXPORT_DATA** in the top right header to download the current state as a `.json` file.
2. Upon returning to the application (or if the worker restarts), click **IMPORT_DATA** and upload the saved file. The system will instantly hydrate all tasks, expenses, and timers.

_(Note: Future iterations can be upgraded to bind a Cloudflare D1 Serverless SQL database directly to the worker for permanent cloud storage)._
