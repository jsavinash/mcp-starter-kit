---
name: database-migration
description: Assess and plan a database schema migration if a persistence feature is deliberately added to this MCP starter. The current repository has no database or migration framework.
---

# Database migration

1. Read `.codex/skills/db_migrate.md` and confirm that the repository now has a database dependency, schema, and migration tool. If not, stop and report that migration is not applicable; do not invent a database command.
2. Identify target environment, migration owner, backup/recovery plan, data volume, rolling-deploy compatibility, and destructive operations.
3. Generate or inspect the migration using the selected project's documented tool. Review SQL/schema changes and lockfile updates before execution.
4. Test upgrade and recovery against a disposable database. Never use production credentials for tests.
5. Inspect status/plan output, confirm target environment, and require explicit authorization for production or destructive execution.
6. Report exact commands/results without printing credentials. Never reset/drop/truncate production data as routine cleanup.
