# scripts/

Utility scripts for development, operations, and data management.

## Planned Scripts

| Script | Purpose |
|---|---|
| `setup_dev.sh` | One-command local dev environment setup |
| `run_migrations.sh` | Apply Alembic DB migrations |
| `seed_db.py` | Seed database with test/demo data |
| `check_env.py` | Validate `.env` has all required variables |
| `download_models.py` | Download required NLP model weights |
| `purge_uploads.py` | Clean up old temporary resume uploads |

## Usage

Scripts are standalone and should document their usage at the top of the file. Run from the repository root:

```bash
python scripts/check_env.py
bash scripts/setup_dev.sh
```

> ⚠️ Never hardcode secrets in scripts. Always read from environment variables.
