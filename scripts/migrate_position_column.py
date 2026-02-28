from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


def resolve_db_path(db_arg: str | None) -> Path:
    if db_arg:
        return Path(db_arg).expanduser().resolve()
    return (Path(__file__).resolve().parents[1] / "hockey.db").resolve()


def get_columns(connection: sqlite3.Connection, table: str) -> list[str]:
    rows = connection.execute(f"PRAGMA table_info({table})").fetchall()
    return [row[1] for row in rows]


def migrate_position_column(db_path: Path) -> None:
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {db_path}")

    with sqlite3.connect(db_path) as connection:
        columns = get_columns(connection, "bio")

        if "position" in columns:
            print("No migration needed: column 'position' already exists in table 'bio'.")
            return

        if "postion" not in columns:
            print("No migration applied: neither 'position' nor 'postion' exists in table 'bio'.")
            return

        connection.execute("ALTER TABLE bio RENAME COLUMN postion TO position")
        connection.commit()
        print("Migration complete: renamed 'bio.postion' to 'bio.position'.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rename bio.postion to bio.position in the SQLite database."
    )
    parser.add_argument(
        "--db",
        dest="db_path",
        default=None,
        help="Path to SQLite DB file (defaults to repo-root hockey.db)",
    )

    args = parser.parse_args()
    db_path = resolve_db_path(args.db_path)

    try:
        migrate_position_column(db_path)
    except FileNotFoundError as error:
        raise SystemExit(str(error))


if __name__ == "__main__":
    main()
