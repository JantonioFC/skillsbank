# Índice de Repositorios de Origen

Este documento centraliza los orígenes de todas las habilidades importadas en el catálogo de Antigravity Awesome Skills. El inventario estructurado se encuentra en [SOURCES.json](SOURCES.json).

## Repositorios Principales

| Repositorio | Autor | Categorías | Método de Sincronización |
| :--- | :--- | :--- | :--- |
| [Azure Agent Skills](https://github.com/microsoft/azure-agent-skills) | Microsoft | Cloud, Azure | `sync_microsoft_skills.sh` |
| [Superpowers](https://github.com/obra/superpowers) | obra | Workflow, Agentic | `npx skills add` |
| [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills) | Vercel Labs | Frontend, React | `npx skills add` |
| [Inference.sh Skills](https://github.com/inference-sh-0/skills) | Inference.sh | AI Tools, Multimedia | `npx skills add` |
| [Browser Use](https://github.com/browser-use/browser-use) | Browser Use | Automation, Browser | `npx skills add` |
| [Squirrel Scan](https://github.com/squirrelscan/skills) | SquirrelScan | Security, Audit | `npx skills add` |
| [Interface Design](https://github.com/dammyjay93/interface-design) | dammyjay93 | Design, UI | `npx skills add` |

## Mantenimiento

Para actualizar las habilidades de un repositorio específico, se recomienda utilizar:
```bash
npx skills upgrade <owner>/<repo>
```

Para el set de Microsoft, utilizar el script dedicado:
```bash
./scripts/sync_microsoft_skills.sh
```

---
*Última actualización sincronizada: 2026-02-15*
