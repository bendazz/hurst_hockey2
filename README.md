# hurst_hockey2

## One-time DB migration

If your existing `hockey.db` still has the old `bio.postion` column name, run:

python scripts/migrate_position_column.py

Optional custom database path:

python scripts/migrate_position_column.py --db /path/to/hockey.db