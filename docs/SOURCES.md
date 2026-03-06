# 🗂️ Índice de Repositorios de Origen

Este documento centraliza los orígenes de las **953 habilidades** importadas en el catálogo de Antigravity Awesome Skills. El inventario detallado y estructurado se encuentra en [SOURCES.json](SOURCES.json).

| Skill / Category            | Original Source                                                            | License        | Notes                         |
| :-------------------------- | :------------------------------------------------------------------------- | :------------- | :---------------------------- |
| `cloud-penetration-testing` | [HackTricks](https://book.hacktricks.xyz/)                                 | MIT / CC-BY-SA | Adapted for agentic use.      |
| `active-directory-attacks`  | [HackTricks](https://book.hacktricks.xyz/)                                 | MIT / CC-BY-SA | Adapted for agentic use.      |
| `owasp-top-10`              | [OWASP](https://owasp.org/)                                                | CC-BY-SA       | Methodology adapted.          |
| `burp-suite-testing`        | [PortSwigger](https://portswigger.net/burp)                                | N/A            | Usage guide only (no binary). |
| `crewai`                    | [CrewAI](https://github.com/joaomdmoura/crewAI)                            | MIT            | Framework guides.             |
| `langgraph`                 | [LangGraph](https://github.com/langchain-ai/langgraph)                     | MIT            | Framework guides.             |
| `react-patterns`            | [React Docs](https://react.dev/)                                           | CC-BY          | Official patterns.            |
| **All Official Skills**     | [Anthropic / Google / OpenAI / Microsoft / Supabase / Apify / Vercel Labs] | Proprietary    | Usage encouraged by vendors.  |

| Repositorio | Autor | Especialidad | Método |
| :--- | :--- | :--- | :--- |
| [Azure Agent Skills](https://github.com/microsoft/azure-agent-skills) | Microsoft | Cloud & Enterprise | Script |
| [Superpowers](https://github.com/obra/superpowers) | obra | Workflow & Patterns | `npx` |
| [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills) | Vercel Labs | Frontend & React | `npx` |
| [Vercel Skills](https://github.com/vercel-labs/skills) | Vercel Labs | Search & Discovery | `npx` |
| [Inference.sh Skills](https://github.com/inference-sh-0/skills) | Inference.sh | AI & Multimedia | `npx` |
| [Browser Use](https://github.com/browser-use/browser-use) | Browser Use | Browser Automation | `npx` |
| [Squirrel Scan](https://github.com/squirrelscan/skills) | SquirrelScan | Security Audit | `npx` |
| [Interface Design](https://github.com/dammyjay93/interface-design) | dammyjay93 | UI/UX Design | `npx` |
| [WShobson Agents](https://github.com/wshobson/agents) | wshobson | .NET & Orchestration | `npx` |

## 🛠️ Guía de Mantenimiento

Para mantener el catálogo actualizado con las últimas novedades de cada origen:

1. **Sincronización General:**
   ```bash
   npx skills upgrade <owner>/<repo>
   ```

2. **Sincronización Microsoft (Específica):**
   ```bash
   ./scripts/sync_microsoft_skills.sh
   ```

3. **Auditoría de Seguridad Post-Importación:**
   ```bash
   python3 scripts/validate_skills.py --strict
   ```

---
*Última auditoría completa: 2026-02-15*
*Total de habilidades verificadas: 953*
