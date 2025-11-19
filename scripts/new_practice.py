"""Create a new practice module from the template."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = REPO_ROOT / "templates" / "practice_template.py"
PRACTICE_DIR = REPO_ROOT / "src" / "py_concurrency" / "practice"


def snake_to_title(name: str) -> str:
    parts = [part for part in name.strip().split("_") if part]
    return " ".join(part.capitalize() for part in parts) if parts else name.capitalize()


def create_practice_file(name: str, *, overwrite: bool) -> Path:
    if not re.fullmatch(r"[a-zA-Z0-9_]+", name):
        msg = "Practice name must only contain letters, digits, or underscores"
        raise ValueError(msg)

    destination = PRACTICE_DIR / f"{name}.py"
    if destination.exists() and not overwrite:
        raise FileExistsError(
            f"{destination.relative_to(REPO_ROOT)} already exists. Use --overwrite to replace it."
        )

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    rendered = template.replace("{title}", snake_to_title(name))
    destination.write_text(rendered, encoding="utf-8")
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="snake_case module name, e.g. fan_in_queue")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite the destination file when it already exists",
    )
    args = parser.parse_args()

    try:
        created_path = create_practice_file(args.name, overwrite=args.overwrite)
    except Exception as exc:  # noqa: BLE001 - surfacing friendly error to the CLI
        parser.error(str(exc))
        return

    rel_path = created_path.relative_to(REPO_ROOT)
    print(f"Created {rel_path}\nRun python -m py_concurrency.practice.{args.name} to start coding.")


if __name__ == "__main__":
    main()
