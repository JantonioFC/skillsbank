---
name: project-docs-orchestrator
description: "Trigger: documentar proyecto, generar documentación, crear suite PRD/RFC/ADR/FSD, scaffolding de docs. Orquesta los 10 documentos de proyecto iterativamente, en orden de dependencia, usando las plantillas del usuario."
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## Activation Contract

Use when the user wants to document a project with the full standard suite
(PRD → ... → System Prompt). For a single document, use the matching
`doc-*-template` skill instead — not this orchestrator.

## Hard Rules

- The template files on disk are the single source of truth. Read the real
  template before each document; never invent structure or copy templates here.
- Generate documents in the dependency order from `assets/template-map.md`.
- Iterative gate: generate a draft → show it → wait for the user's approval or
  edits → only then advance. Never produce the next document without an OK.
- Each document reads the already-approved docs it depends on, so the suite
  stays coherent (the FSD must speak the PRD's language).
- Write documents in the same language as the templates (Spanish). Replace every
  `[placeholder]` and illustrative example with real project content.

## Decision Gates

| Situation | Action |
|-----------|--------|
| Project context still vague before a doc | Ask only the questions that doc needs, then draft |
| User edits a draft | Save the edited version as the approved source for downstream docs |
| User skips a document | Record it as skipped; downstream docs read only what exists |
| `TEMPLATES_DIR` missing or moved | Stop and confirm the path with the user |

## Execution Steps

1. Ask for the project name and the destination folder.
2. Scaffolding: create the folder and copy the 10 templates as empty molds,
   renamed per the output convention in `assets/template-map.md`.
3. For each document in dependency order:
   a. Read its template and the approved docs it depends on.
   b. Draft it, filling placeholders with real project content.
   c. Show the draft; collect edits or approval. Do not advance without an OK.
   d. Save the approved version into the project folder.
4. Close with a status list of the 10 documents (approved / skipped / pending).

## Output Contract

Return: project folder path, documents approved, documents skipped or pending,
and the next document to generate.

## References

- `assets/template-map.md` — dependency graph, template filenames, `TEMPLATES_DIR`.
