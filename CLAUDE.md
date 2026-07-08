# Language

- All user-facing output (explanations, reports, code comments, docs, commit messages) is in Korean by default.
- Keep technical terms, commands, API names, and identifiers in English.

# Principles

- Mark uncertain information as "확인 필요" — never fabricate. Verify anything that changes over time (versions, supported models, pricing, vendor policies) against official docs.
- Keep answers concise. No unrequested explanations or alternative listings.

# Safety

- Work only inside this repository. Ask before: modifying files outside the repo, using sudo, changing system config, or deleting/modifying production resources.
- Never commit secrets, API keys, tokens, or real env files. Document required variables in `.env.example`.
- Install dependencies in a project-local virtualenv with pinned versions (`requirements.txt` or `pyproject.toml`).
- Run relevant tests/typecheck/lint before reporting completion. If none exist, at least verify the code runs.

# Code

- Implement the minimum requested. No unrequested features, options, abstractions, or future-proofing.
- Korean comments on core or non-obvious logic only; none on self-evident code.
- Prefer editing existing files over creating new ones. Follow existing code style and structure.
- Handle only errors that can actually occur. Never hide errors with broad try/except.

# Refactoring

- Behavior (input/output) must not change. Never mix refactoring with feature changes in one commit.
- Stop if the result would be longer than the original.
- Priority: dead code removal > deduplication > hardcoded values > naming > structure.
- Verify behavior with tests (or a run check) before and after. Report a change summary table (location / before → after / reason).

# Infra

- Use only syntax supported by the current environment versions; flag anything uncertain.
- No `:latest` tags, root execution, or hardcoded secrets.
- Provide verification commands (dry-run, lint, plan) before applying.

# Branches

- Never commit directly to main/master. Work on task branches.
- Before starting any task, check that the current branch matches the task. If not, propose the correct branch and switch (checkout) after user confirmation. Carry uncommitted changes safely (stash) when switching.
- If accumulated changes exceed the current branch's scope — unrelated files touched, multiple concerns mixed — pause, report it, and propose splitting into a new branch with a suggested name.

# Project start (proactive)

When starting a new project — no `.git` directory exists, or the user says they are starting one — proactively run the `/시작` sequence below (each step after user confirmation). Also print the workflow reminder whenever a project kicks off:

```
작업 흐름: /브랜치 → 작업 → /정리 → /점검 → /푸시(PR 판정) → /PR → /clear
```

# Session hygiene (proactive)

`/clear` and `/compact` are built-in commands only the user can run. Never run them yourself — suggest them at the right moment, in one line, with the reason:

- After `/푸시` completes: suggest `/clear` (natural end of a work unit).
- When the topic shifts to an unrelated task, or previously read files are no longer relevant: suggest `/clear`.
- When the session is long but continuing context is still needed: suggest `/compact` instead.
- Rule of thumb: one commit = one work unit = one session.

# PR rules (proactive)

Do not let PR timing slip. Evaluate PR readiness at every `/푸시` and whenever asked about branch status, and report one of:

- **PR now**: the branch's task scope is complete, or 3+ commits / significant diff vs the base branch has accumulated.
- **PR soon**: scope is nearly done — state what remains before PR.
- **Not yet**: work in progress, no action.

When "PR now", immediately suggest running `/PR`. A branch should live days, not weeks — flag any branch that keeps growing without a PR.

# Commands

- `/시작`: Project kickoff sequence — ① `git status` check; if not a repo, `git init` (default branch `main`) ② create `.gitignore` (Python/env) and `.env.example` if missing ③ if no remote, ask public/private (default private) and create a GitHub repo with `gh repo create <name> --private --source=. --remote=origin`; if `gh` is unavailable, guide manual repo creation + `git remote add origin <url>` ④ initial commit and push after confirmation ⑤ print the workflow reminder (`/브랜치 → 작업 → /정리 → /점검 → /푸시 → /PR → /clear`).
- `/정리`: Refactor recently written/modified code per the refactoring rules; report the change summary.
- `/푸시`: Verify current branch is correct for the task → run tests/lint → if all pass, commit and push the current branch to remote → evaluate PR readiness (see PR rules) → suggest `/clear` if the work unit is done.
- `/점검`: Scan for exposed secrets, committed env files, dead code, and TODOs. Report only — do not modify.
- `/브랜치`: Show current branch and uncommitted changes → judge whether the branch matches the current task → if mismatched, propose and switch after confirmation → if changes have outgrown the branch scope, propose a new branch (with name) and how to split the changes.
- `/PR`: Diff current branch against the base branch → summarize changes → draft PR title and description in Korean (what/why/how-to-verify) → after user confirmation, create the PR with `gh pr create`; if `gh` is unavailable, output the draft for manual creation.
