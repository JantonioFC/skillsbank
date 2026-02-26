---
name: wiki-onboarding
description: "Generates two complementary onboarding guides \u2014 a Principal-Level architectural deep-dive and a Zero-to-Hero contributor walkthrough. Use when the user wants onboarding documentation fo..."
risk: unknown
source: community
---

# Wiki Onboarding Guide Generator

> **⚠️ AUTHORIZED USE ONLY**
> This skill is for educational purposes or authorized security assessments only.
> You must have explicit, written permission from the system owner before using this tool.
> Misuse of this tool is illegal and strictly prohibited.

Generate four audience-tailored onboarding documents in an `onboarding/` folder, each giving a different stakeholder exactly the understanding they need.

## Source Repository Resolution (MUST DO FIRST)

Before generating any guides, you MUST determine the source repository context:

1. **Check for git remote**: Run `git remote get-url origin` to detect if a remote exists
2. **Ask the user**: _"Is this a local-only repository, or do you have a source repository URL (e.g., GitHub, Azure DevOps)?"_
   - Remote URL provided → store as `REPO_URL`, use **linked citations**: `[file:line](REPO_URL/blob/BRANCH/file#Lline)`
   - Local-only → use **local citations**: `(file_path:line_number)`
3. **Determine default branch**: Run `git rev-parse --abbrev-ref HEAD`
4. **Do NOT proceed** until source repo context is resolved

## When to Activate

- User asks for onboarding docs or getting-started guides
- User runs `/deep-wiki:onboard` command
- User wants to help new team members understand a codebase

## Output Structure

Generate an `onboarding/` folder with these files:

```
onboarding/
├── index.md                    # Onboarding hub — links to all 4 guides with audience descriptions
├── contributor-guide.md        # For new contributors (assumes Python or JS background)
├── staff-engineer-guide.md     # For staff/principal engineers
├── executive-guide.md          # For VP/director-level engineering leaders
└── product-manager-guide.md    # For product managers and non-engineering stakeholders
```

### `index.md` — Onboarding Hub

A landing page with:
- **One-paragraph project summary**
- **Guide selector table**:

| Guide | Audience | What You'll Learn | Time |
|-------|----------|-------------------|------|
| [Contributor Guide](./contributor-guide.md) | New contributors with Python/JS experience | Setup, first PR, codebase patterns | ~30 min |
| [Staff Engineer Guide](./staff-engineer-guide.md) | Staff/principal engineers | Architecture, design decisions, system boundaries | ~45 min |
| [Executive Guide](./executive-guide.md) | VP/directors of engineering | Capabilities, risks, team topology, investment thesis | ~20 min |
| [Product Manager Guide](./product-manager-guide.md) | Product managers | Features, user journeys, constraints, data model | ~20 min |

## Language Detection

Scan the repository for build files to determine the primary language for code examples:
- `package.json` / `tsconfig.json` → TypeScript/JavaScript
- `*.csproj` / `*.sln` → C# / .NET
- `Cargo.toml` → Rust
- `pyproject.toml` / `setup.py` / `requirements.txt` → Python
- `go.mod` → Go
- `pom.xml` / `build.gradle` → Java

---

## Guide 1: Contributor Guide

**File**: `onboarding/contributor-guide.md`
**Audience**: Engineers joining the project. Assumes proficiency in Python or JavaScript and general software engineering experience.
**Length**: 1000–2500 lines. Progressive — each section builds on the last.

### Required Sections

**Part I: Foundations** (skip if repo uses Python or JS)
1. **{Primary Language} for Python/JS Engineers** — Syntax comparison tables, async model, collections, type system, package management. Concrete code side-by-side, NOT abstract descriptions.
2. **{Primary Framework} Essentials** — Compare to equivalent Python/JS frameworks (e.g., FastAPI, Express). Request pipeline, routing, DI, config.

**Part II: This Codebase**
3. **What This Project Does** — 2-3 sentence elevator pitch
4. **Project Structure** — Annotated directory tree (what lives where and why). Include `graph TB` architecture overview.
5. **Core Concepts** — Domain-specific terminology explained with code examples. Use `erDiagram` for data model.
6. **Request Lifecycle** — `sequenceDiagram` (with `autonumber`) tracing a typical request end-to-end.
7. **Key Patterns** — "If you want to add X, follow this pattern" templates with real code

**Part III: Getting Productive**
8. **Prerequisites & Setup** — Table: Tool, Version, Install Command. Step-by-step with expected output at each step.
9. **Your First Task** — End-to-end walkthrough of adding a simple feature
10. **Development Workflow** — Branch strategy, commit conventions, PR process. Use `flowchart` diagram.
11. **Running Tests** — All tests, single file, single test, coverage commands
12. **Debugging Guide** — Common issues table: Symptom, Cause, Fix
13. **Common Pitfalls** — Mistakes every new contributor makes and how to avoid them

**Appendices**
- **Glossary** (40+ terms)
- **Key File Reference** — Table: Path, Purpose, Why It Matters, Source
- **Quick Reference Card** — Cheat sheet of most-used commands and patterns

### Rules
- All code examples in the detected primary language
- Every command must be copy-pasteable
- Include expected output for verification steps
- Use Mermaid for workflow diagrams (dark-mode colors)
- Ground all claims in actual code — cite `(file_path:line_number)`

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.
