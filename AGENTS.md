# AGENTS.md

## Project Overview

This repository contains a software project. Before making changes, read the README, project documentation, and nearby code to understand the intended workflow, architecture, and conventions.

## Working Principles

- Prefer the repository's existing patterns, naming, and tools over introducing new conventions.
- Keep changes focused on the user's request; avoid opportunistic refactors unless they are necessary for correctness or maintainability.
- Preserve behavior unless the task explicitly asks for a behavior change.
- Treat the working tree as shared: do not revert or overwrite changes you did not make.
- When requirements are ambiguous, choose the smallest reasonable implementation and document assumptions.

## Project Structure

- Keep the project structure easy to scan and document the purpose of important top-level folders.
- Separate source code, tests, documentation, configuration, generated artifacts, and local data/cache files where possible.
- Put reusable implementation logic in the project's source package or shared module area.
- Keep one-off, workflow-specific, experiment-specific, or notebook-specific logic close to the workflow that uses it.
- Do not move code into shared `src` modules just because it is convenient; shared code should be generic, reusable, and stable enough to import from multiple places.

## Setup and Dependencies

- Use the package manager and environment tooling already present in the repository.
- Update lockfiles when dependency changes require it.
- Do not add new dependencies when the standard library or existing project dependencies are sufficient.
- Document required setup commands in the README or another visible project document.

## Code Quality

- Prefer clear, direct code over clever abstractions.
- Add abstractions only when they remove real duplication or clarify a stable boundary.
- Keep functions small enough to understand, with names that describe intent.
- Use structured APIs and parsers for structured data instead of fragile string manipulation.
- Add comments only where they explain non-obvious reasoning, constraints, or trade-offs.

## Tests and Validation

- Run the narrowest relevant checks after a change, then broader checks when the change affects shared behavior.
- Add or update tests when changing behavior, fixing a bug, or touching shared logic.
- If tests cannot be run, state what was not run and why.
- For notebooks or generated documents, clear noisy outputs unless the project intentionally tracks them.

## Data, Secrets, and Generated Files

- Do not commit secrets, credentials, local environment files, or private tokens.
- Do not commit large data files, caches, build outputs, or generated artifacts unless the project explicitly tracks them.
- Keep generated files in documented locations and make regeneration steps clear.
- Avoid changing source data or persisted outputs unless the task explicitly requires it.

## Documentation

- Keep documentation aligned with code behavior, file names, commands, and data contracts.
- Update README or reference docs when changing workflow order, public interfaces, configuration, or generated outputs.
- Preserve historical notes unless the task is specifically to revise them.

## Git and Collaboration

- Use short, imperative commit messages when commits are requested.
- Do not create commits unless explicitly asked.
- Before committing, review the full diff and avoid including unrelated files.
- Prefer topic branches with descriptive names for substantial work.

## Reviews

- For code review requests, prioritize bugs, regressions, security issues, data loss risks, and missing tests.
- Report findings first, ordered by severity, with file references and concrete impact.
- If no issues are found, say so and mention any residual risk or checks not performed.
