# py-concurrency

Playground for experimenting with Python concurrency primitives (threads, processes, asyncio, queues, etc.).
The repository ships with a light scaffold so new experiments can be added quickly without repeating setup work.

## Environment setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e ".[dev]"
```

Useful commands after activation:

```bash
pytest              # run tests under tests/
ruff check          # lint
ruff format         # auto-format
```

## Repository layout

```
.
├── src/py_concurrency/        # Package containing practice modules and helpers
│   ├── practice/              # Drop new practice files here
│   └── utils/                 # Shared helpers (e.g., timing decorator)
├── templates/                 # Skeletons that scripts/new_practice.py copies from
├── scripts/                   # Small helpers (e.g., create new practice)
└── tests/                     # Optional regression or learning tests
```

Each practice module is an executable script (e.g. `python -m py_concurrency.practice.thread_pool_basics`).
Keeping everything inside `src/` lets tools (pytest, coverage, etc.) discover the package automatically.

## Creating a new practice module

Use the helper script to copy the template into `src/py_concurrency/practice/`:

```bash
python scripts/new_practice.py fan_in_queue
```

The script validates the module name, populates metadata, and drops you into an already wired main function
with sequential/concurrent placeholders. You can still copy files manually if you prefer.

## Included helpers

- `PracticeTemplate`: demonstrates the expected structure of a runnable exercise.
- `timed` decorator logs duration for sequential vs. concurrent solutions.
- `thread_pool_basics` example uses `concurrent.futures` to show how the scaffold is intended to be used.

Add more utilities (profilers, fake workloads, etc.) under `src/py_concurrency/utils/` and import them from your
practice modules when needed.
