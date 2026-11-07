# Database migration recipe

> Current status: this starter kit has no database dependency, schema, or migration framework. This recipe is a future workflow and a no-op until a database-backed feature is intentionally added.

## Before adding migrations

1. Confirm the feature requires persistence and identify the database, supported deployment topology, and data-retention requirements.
2. Propose the database client and migration tool as explicit workspace dependencies. Document why they belong in the app or shared library.
3. Define ownership, connection settings, secret handling, pooling, health checks, and lifecycle cleanup.
4. Choose a migration workflow compatible with local development and production release orchestration. Do not execute migrations automatically on server startup.
5. Update architecture and operations docs before committing schema or migration commands.

## Migration review checklist

- [ ] Migration is versioned, deterministic, and reviewed alongside the model/schema change.
- [ ] Upgrade and rollback/recovery behavior is documented; destructive or lossy operations have a staged plan.
- [ ] Large-table changes are safe for the expected data volume and deployment window.
- [ ] Application versions can coexist during rolling deployments where required.
- [ ] Credentials are injected at runtime and never committed or printed.
- [ ] Tests cover the migration on an isolated disposable database, if infrastructure is available.
- [ ] Backup/restore and operational ownership are documented for production.

## Execution rules

- Inspect the migration tool's plan/status output before applying a change.
- Never reset, drop, truncate, downgrade production data, or apply destructive migrations without explicit user authorization and a reviewed recovery plan.
- Do not run a migration against a configured external database as part of routine validation.
- Record the exact target environment and command used. Redact connection strings and credentials.

Until these prerequisites are met, report database migration as not applicable rather than inventing a database command.
