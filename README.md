# abstract_database

**Lazy, environment-driven PostgreSQL connection management with multi-database
support and table/query helpers.**

`abstract_database` is the connection layer of the **Abstract Secure Backend**
stack. It resolves connection settings from your environment, manages
connections to one or many databases, and provides thin helpers for tables and
queries — without ever forcing a database connection before you actually need
one.

---

## Where this fits

```
abstract-securefiles   React/TypeScript UI components
abstract_logins        Flask blueprints: auth + secure files
abstract_queries       Domain query managers (users, uploads, ...)
abstract_database  <-- you are here: lazy PostgreSQL connection + helpers
abstract_security      Env loading, hashing, tokens, utilities
```

Dependencies flow downward; nothing reaches back up.

---

## Install

```bash
pip install abstract_database
```

Requires Python ≥ 3.11 and PostgreSQL (uses `psycopg[binary]`).

---

## Configuration

Connection settings are read from the environment, so the package is portable
across machines. Per-database keys follow `<DBNAME>_<DBTYPE>_<FIELD>`
(upper-cased), or you can supply a single URL:

```ini
ABSTRACT_DATABASE_USER=app_user
ABSTRACT_DATABASE_PASSWORD=...
ABSTRACT_DATABASE_HOST=127.0.0.1
ABSTRACT_DATABASE_PORT=5432
ABSTRACT_DATABASE_DBNAME=app
# or:
ABSTRACT_DATABASE_URL=postgresql://app_user:...@127.0.0.1:5432/app
```

Optional locations:

| Variable | Purpose |
|---|---|
| `ABSTRACT_DB_ENV_PATH` | Path to the `.env` file to read. |
| `ABSTRACT_DB_TABLES_DIR` | Directory holding table-config JSON. |
| `ABSTRACT_DB_TYPE` | Default db-type label (default `database`). |

---

## Quickstart

```python
from abstract_database import connectionManager, get_cur_conn

# Constructing a manager does NOT open a connection.
db = connectionManager(dbName="app", dbType="database")

# The connection opens on first use; failures raise a clear ConnectionError.
cur, conn = get_cur_conn()           # RealDict cursor + connection
cur.execute("SELECT 1;")
print(cur.fetchone())
conn.close()
```

### Multiple databases

```python
users = connectionManager(dbName="app",      dbType="database")
audit = connectionManager(dbName="auditlog", dbType="database")
# Distinct, independently-configured managers — no global clobbering.
```

---

## Design notes

- **Lazy by default.** Constructing a `connectionManager` never touches the
  database. The connection opens on first real use, so importing the package or
  booting an app never blocks (or fails) on an unreachable database. Table setup
  is deferred behind `ensure_inserts()`.
- **Multi-DB safe.** Managers are cached by connection identity (name / type /
  env-path / url) rather than a single global singleton, so several databases
  coexist cleanly. A no-argument `connectionManager()` still maps to one shared
  default.
- **Failures are visible.** `connect_db()` raises a `ConnectionError` with the
  underlying cause instead of silently returning `None` and breaking three calls
  later.

---

## License

MIT.
