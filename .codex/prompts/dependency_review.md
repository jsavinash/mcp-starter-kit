# Dependency review prompt

Review proposed dependency changes for this Python `uv` monorepo.

- Confirm direct dependency ownership: root tooling vs app runtime vs shared core vs optional extra.
- Prefer official SDK APIs and supported Python versions (`>=3.11`).
- Check upstream project/source, maintenance, license, security advisories, transitive footprint, and whether a standard-library or existing-dependency solution is sufficient.
- Check lower and upper version bounds, Python markers, extras, resolver compatibility, and all affected workspace packages.
- Update metadata and regenerate `uv.lock` with `uv`; never hand-edit generated lock data.
- Identify runtime import changes, image size/startup impact, supply-chain risk, and dependency-audit implications.
- Recommend focused compatibility/security tests and document any excluded versions.

Return the exact files and commands needed. Do not state that a package is secure solely because an audit finds no known advisory.
