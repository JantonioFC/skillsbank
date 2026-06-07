# Template Map & Dependency Graph

Source of truth for templates (read at runtime, never copy into this skill):

```
TEMPLATES_DIR = /home/juan/Escritorio/Codigo Documentado/
```

Generation order. Each document reads the **approved** outputs of the docs it depends on,
so content stays coherent across the suite.

| # | Document | Template file (in TEMPLATES_DIR) | Reads before generating |
|---|----------|----------------------------------|-------------------------|
| 1 | PRD | `Plantilla_ PRD (Documento de Requisitos de Producto).md` | — (root) |
| 2 | User Stories | `Plantilla_ Historias de Usuario (User Stories).md` | PRD |
| 3 | FSD | `Plantilla_ FSD (Especificación Funcional Detallada).md` | PRD, User Stories |
| 4 | BDD/Gherkin | `Plantilla_ Especificación BDD (Gherkin).md` | User Stories, FSD |
| 5 | RFC | `Plantilla_ RFC (Request for Comments).md` | FSD |
| 6 | ADR | `Plantilla_ ADR (Registro de Decisión Arquitectónica).md` | RFC |
| 7 | Plan TDD | `Plantilla_ Plan de Pruebas Unitarias y TDD.md` | BDD/Gherkin, FSD |
| 8 | Infra CI/CD | `Plantilla_ Especificación de Infraestructura y CI_CD.md` | RFC, ADR |
| 9 | DORA Metrics | `Plantilla_ Reporte de Métricas DORA y Salud.md` | Infra CI/CD |
| 10 | System Prompt | `Plantilla_ System Prompt (Orquestador de Ingeniería).md` | all approved docs |

Output naming convention (in the project folder):
`<NN> - <Document> - <ProjectName>.md` (e.g. `01 - PRD - Cortex.md`).
