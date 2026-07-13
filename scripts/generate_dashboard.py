import os
import json
import re

OUTPUT_FILE = "docs/DASHBOARD.html"

# Cargar traducciones si existen
TRANSLATIONS_FILE = "docs/translations_es.json"
TRANSLATIONS = {}
if os.path.exists(TRANSLATIONS_FILE):
    try:
        with open(TRANSLATIONS_FILE, "r", encoding="utf-8") as f:
            TRANSLATIONS = json.load(f)
    except Exception as e:
        print(f"Error cargando traducciones: {e}")

# Traducciones de categorias al castellano
CATEGORY_ES = {
    "infrastructure": "Infraestructura",
    "general": "General",
    "development": "Desarrollo",
    "security": "Seguridad",
    "data-ai": "Datos e IA",
    "testing": "Pruebas",
    "business": "Negocio",
    "workflow": "Flujos de trabajo",
    "architecture": "Arquitectura",
}

# Traducciones de subcategorias al castellano
SUBCATEGORY_ES = {
    # infrastructure
    "containers": "Contenedores",
    "observability": "Observabilidad",
    "messaging": "Mensajeria y eventos",
    "ci-cd": "CI/CD y despliegue",
    "cloud-services": "Servicios en la nube",
    "infra-general": "Infra general",
    # general
    "game-dev": "Desarrollo de juegos",
    "code-quality": "Calidad de codigo",
    "docs-formats": "Documentos y formatos",
    "design-ux": "Diseno y UX",
    "agent-tools": "Herramientas de agentes",
    "general-misc": "General miscelaneo",
    # development
    "python": "Python",
    "frontend": "Frontend",
    "fp-ts": "Programacion funcional",
    "mobile": "Movil",
    "azure-sdk": "Azure SDK",
    "dev-general": "Desarrollo general",
    # fallback
    "(sin subcategoria)": "(sin subcategoria)",
}

# Traducciones heuristicas para descripciones
TRANSLATION_RULES = [
    # Frases completas primero
    (r'\bUse when\b', 'Usar cuando'),
    (r'\bUse for\b:?', 'Usar para:'),
    (r'\bUse this skill when\b', 'Usar esta habilidad cuando'),
    (r'\bUse PROACTIVELY\b', 'Usar PROACTIVAMENTE'),
    (r'\bCovers\b:?', 'Incluye:'),
    (r'\bTriggers\b:?', 'Activadores:'),
    (r'\bHow to\b', 'Cómo'),
    (r'\bBest practices\b', 'Mejores prácticas'),
    (r'\bExpert in\b', 'Experto en'),
    (r'\bSpecializing in\b', 'Especializado en'),
    (r'\bMaster\b', 'Dominio de'),
    (r'\bWrite idiomatic\b', 'Escribir código idiomático en'),
    (r'\bBuild and deploy\b', 'Construir y desplegar'),
    (r'\bBuild scalable\b', 'Construir escalable'),
    (r'\bDesign and implement\b', 'Diseñar e implementar'),
    (r'\bCreate and manage\b', 'Crear y gestionar'),
    (r'\bAutomate\b', 'Automatizar'),
    (r'\bConfigure and optimize\b', 'Configurar y optimizar'),
    (r'\bAnalyze and\b', 'Analizar y'),
    (r'\bMonitor and\b', 'Monitorizar y'),
    # Sustantivos / conceptos
    (r'\bManagement\b', 'Gestión'),
    (r'\bOptimization\b', 'Optimización'),
    (r'\bImplementation\b', 'Implementación'),
    (r'\bIntegration\b', 'Integración'),
    (r'\bCreation\b', 'Creación'),
    (r'\bAnalysis\b', 'Análisis'),
    (r'\bTesting\b', 'Pruebas'),
    (r'\bDeployment\b', 'Despliegue'),
    (r'\bMonitoring\b', 'Monitorización'),
    (r'\bAuthentication\b', 'Autenticación'),
    (r'\bAuthorization\b', 'Autorización'),
    (r'\bConfiguration\b', 'Configuración'),
    (r'\bDocumentation\b', 'Documentación'),
    (r'\bPerformance\b', 'Rendimiento'),
    (r'\bSecurity\b', 'Seguridad'),
    (r'\bArchitecture\b', 'Arquitectura'),
    (r'\bDevelopment\b', 'Desarrollo'),
    (r'\bApplication\b', 'Aplicación'),
    (r'\bApplications\b', 'Aplicaciones'),
    (r'\bDatabase\b', 'Base de datos'),
    (r'\bDatabases\b', 'Bases de datos'),
    (r'\bpatterns\b', 'patrones'),
    (r'\bguidelines\b', 'guías'),
    (r'\bframework\b', 'marco de trabajo'),
    (r'\bSkill\b', 'Habilidad'),
    (r'\bWorkflow\b', 'Flujo de trabajo'),
    (r'\bWorkflows\b', 'Flujos de trabajo'),
    (r'\bDebugging\b', 'Depuración'),
    (r'\bRefactoring\b', 'Refactorización'),
    (r'\bScaffolding\b', 'Scaffolding'),
    (r'\bObservability\b', 'Observabilidad'),
    (r'\bReliability\b', 'Fiabilidad'),
    (r'\bAvailability\b', 'Disponibilidad'),
    (r'\bScalability\b', 'Escalabilidad'),
    (r'\bMaintainability\b', 'Mantenibilidad'),
    (r'\bAccessibility\b', 'Accesibilidad'),
    (r'\bCompliance\b', 'Cumplimiento'),
    (r'\bVulnerability\b', 'Vulnerabilidad'),
    (r'\bVulnerabilities\b', 'Vulnerabilidades'),
    (r'\bincluding\b', 'incluyendo'),
    (r'\bspecialist\b', 'especialista'),
    (r'\bspecializing\b', 'especializado en'),
    (r'\bcomprehensive\b', 'integral'),
    (r'\badvanced\b', 'avanzado'),
    (r'\bmodern\b', 'moderno'),
    (r'\bproduction\b', 'producción'),
    (r'\bresponsive\b', 'responsivo'),
    (r'\bscalable\b', 'escalable'),
    (r'\band\b', 'y'),
    (r'\bwith\b', 'con'),
    (r'\bfor\b', 'para'),
    (r'\busing\b', 'usando'),
    (r'\bbased on\b', 'basado en'),
]

def translate_text(text):
    if not text: return "Sin descripción"
    for pattern, replacement in TRANSLATION_RULES:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


def translate_category(cat):
    return CATEGORY_ES.get(cat, cat.replace("-", " ").title())


def translate_subcategory(sub):
    return SUBCATEGORY_ES.get(sub, sub.replace("-", " ").title())


def get_skill_data():
    """Load skills from skills_index.json (generated by generate_index.py)."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    index_path = os.path.join(base_dir, "skills_index.json")

    with open(index_path, "r", encoding="utf-8") as f:
        raw_skills = json.load(f)

    skills = []
    for s in raw_skills:
        name = s.get("name", s["id"])
        description = s.get("description", "")

        # Traducciones heuristicas o desde archivo
        if name in TRANSLATIONS:
            description = TRANSLATIONS[name].get("description", description)
        else:
            description = translate_text(description)

        if len(description) > 160:
            description = description[:157] + "..."

        skills.append({
            "id": s["id"],
            "name": name,
            "description": description,
            "source": s.get("source", "unknown"),
            "category": s.get("category", "general"),
            "subcategory": s.get("subcategory"),
        })

    return sorted(skills, key=lambda x: x["name"].lower())


def generate_html(skills):
    # Agrupar por categoria -> subcategoria
    categories_dict = {}
    for s in skills:
        c = s["category"]
        if c not in categories_dict:
            categories_dict[c] = {}
        sub = s["subcategory"] or "(sin subcategoria)"
        if sub not in categories_dict[c]:
            categories_dict[c][sub] = []
        categories_dict[c][sub].append(s)

    categories_list = []
    for cat, subs in sorted(categories_dict.items()):
        subcategories = []
        total = 0
        for sub_name, members in sorted(subs.items()):
            subcategories.append({
                "name": translate_subcategory(sub_name),
                "count": len(members),
                "skills": members
            })
            total += len(members)
        has_subcategories = not (len(subcategories) == 1 and subcategories[0]["name"] == "(sin subcategoria)")
        categories_list.append({
            "name": translate_category(cat),
            "count": total,
            "hasSubcategories": has_subcategories,
            "subcategories": subcategories,
            "skills": [sk for sub in subcategories for sk in sub["skills"]]
        })

    html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Awesome Skills - Panel de habilidades</title>
    <style>
        :root {
            --bg: #0d1117;
            --card-bg: #161b22;
            --card-hover: #21262d;
            --text: #c9d1d9;
            --text-bright: #f0f6fc;
            --primary: #58a6ff;
            --accent: #d2a8ff;
            --accent2: #7ee787;
            --border: #30363d;
        }
        body { font-family: -apple-system, sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 0; }
        header { background: #161b22; padding: 20px 40px; border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 20px; }
        header h1 { margin: 0; font-size: 1.5rem; color: var(--primary); }
        .back-btn { background: #21262d; border: 1px solid var(--border); color: var(--text); padding: 8px 16px; border-radius: 6px; cursor: pointer; display: none; }
        .container { max-width: 1200px; margin: 40px auto; padding: 0 20px; }

        .search-bar { margin-bottom: 30px; }
        #search { width: 100%; max-width: 500px; padding: 12px; border-radius: 6px; border: 1px solid var(--border); background: var(--card-bg); color: #fff; }

        .breadcrumb { margin-bottom: 20px; font-size: 0.9rem; color: #8b949e; display: none; }
        .breadcrumb a { color: var(--primary); cursor: pointer; text-decoration: none; }
        .breadcrumb a:hover { text-decoration: underline; }

        .cat-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
        .cat-card { background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; padding: 25px; cursor: pointer; transition: 0.2s; text-align: left; }
        .cat-card:hover { border-color: var(--accent); background: var(--card-hover); }
        .cat-card h2 { margin: 0; color: var(--text-bright); font-size: 1.3rem; }
        .cat-card .badge { display: inline-block; margin-top: 10px; background: #23863622; color: #3fb950; padding: 2px 8px; border-radius: 20px; font-size: 0.8rem; }
        .cat-card .sub-hint { margin-top: 8px; font-size: 0.8rem; color: #8b949e; }

        .sub-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 16px; }
        .sub-card { background: var(--card-bg); border: 1px solid var(--border); border-radius: 10px; padding: 20px; cursor: pointer; transition: 0.2s; }
        .sub-card:hover { border-color: var(--accent2); background: var(--card-hover); }
        .sub-card h3 { margin: 0; color: var(--accent2); font-size: 1.1rem; }
        .sub-card .badge { display: inline-block; margin-top: 8px; background: #23863622; color: #3fb950; padding: 2px 8px; border-radius: 20px; font-size: 0.75rem; }

        .skills-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
        .skill-item { background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; padding: 20px; }
        .skill-item h3 { margin: 0 0 10px 0; color: var(--primary); }
        .skill-item p { font-size: 0.9rem; line-height: 1.4; color: #8b949e; }
        .skill-item .source { margin-top: 15px; font-size: 0.75rem; color: var(--accent); font-weight: bold; }

        .view { display: none; }
        .view.active { display: block; }
    </style>
</head>
<body>
    <header>
        <button id="backBtn" class="back-btn" onclick="goBack()">&#8592; Atrás</button>
        <h1>Panel de Habilidades</h1>
    </header>

    <div class="container">
        <div class="search-bar">
            <input type="text" id="search" placeholder="Buscar skills...">
        </div>

        <div id="breadcrumb" class="breadcrumb"></div>
        <div id="viewCategories" class="view active"><div id="catGrid" class="cat-grid"></div></div>
        <div id="viewSubcategories" class="view"><div id="subGrid" class="sub-grid"></div></div>
        <div id="viewSkills" class="view"><div id="skillsGrid" class="skills-grid"></div></div>
    </div>

    <script>
        const data = %DATA%;
        const allSkills = %ALL_SKILLS%;
        let navStack = []; // track navigation: [{view, title}]

        function escapeHtml(str) {
            return String(str)
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#39;');
        }

        // For interpolating a value as a JS string-literal argument inside a
        // double-quoted HTML attribute (e.g. onclick="fn(...)"). JSON.stringify
        // produces a fully quoted and escaped JS string literal; escapeHtml then
        // makes that literal safe to sit inside the surrounding HTML attribute.
        function escapeForJsAttr(str) {
            return escapeHtml(JSON.stringify(String(str)));
        }

        function showView(viewId) {
            document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
            document.getElementById(viewId).classList.add('active');
        }

        function updateBreadcrumb() {
            const bc = document.getElementById('breadcrumb');
            const backBtn = document.getElementById('backBtn');
            if (navStack.length <= 1) {
                bc.style.display = 'none';
                backBtn.style.display = 'none';
                return;
            }
            bc.style.display = 'block';
            backBtn.style.display = 'block';
            const parts = navStack.map((item, i) => {
                if (i < navStack.length - 1) {
                    return `<a onclick="goTo(${i})">${escapeHtml(item.title)}</a>`;
                }
                return `<span style="color:var(--text-bright)">${escapeHtml(item.title)}</span>`;
            });
            bc.innerHTML = parts.join(' / ');
        }

        function goTo(index) {
            const target = navStack[index];
            navStack = navStack.slice(0, index + 1);
            target.action();
            updateBreadcrumb();
        }

        function goBack() {
            if (navStack.length > 1) {
                goTo(navStack.length - 2);
            }
        }

        function renderSkillCards(skills, container) {
            container.innerHTML = skills.map(s => `
                <div class="skill-item">
                    <h3>${s.name}</h3>
                    <p>${s.description}</p>
                    <div class="source">@${s.source}</div>
                </div>
            `).join('');
        }

        function renderCategories() {
            showView('viewCategories');
            const grid = document.getElementById('catGrid');
            grid.innerHTML = data.map(c => {
                const subHint = c.hasSubcategories
                    ? `<div class="sub-hint">${c.subcategories.length} subcategorías</div>`
                    : '';
                return `
                    <div class="cat-card" onclick="openCat(${escapeForJsAttr(c.name)})">
                        <h2>${escapeHtml(c.name)}</h2>
                        <span class="badge">${c.count} habilidades</span>
                        ${subHint}
                    </div>
                `;
            }).join('');
        }

        function openCat(name) {
            const cat = data.find(c => c.name === name);
            if (!cat) return;

            if (cat.hasSubcategories) {
                // Show subcategories view
                navStack.push({ title: name, action: () => { showView('viewSubcategories'); openCatInner(cat); } });
                openCatInner(cat);
            } else {
                // No subcategories — show skills directly
                navStack.push({ title: name, action: () => { showView('viewSkills'); renderSkillCards(cat.skills, document.getElementById('skillsGrid')); } });
                showView('viewSkills');
                renderSkillCards(cat.skills, document.getElementById('skillsGrid'));
            }
            updateBreadcrumb();
            window.scrollTo(0, 0);
        }

        function openCatInner(cat) {
            showView('viewSubcategories');
            const grid = document.getElementById('subGrid');
            grid.innerHTML = cat.subcategories.map(sub => `
                <div class="sub-card" onclick="openSub(${escapeForJsAttr(cat.name)}, ${escapeForJsAttr(sub.name)})">
                    <h3>${escapeHtml(sub.name)}</h3>
                    <span class="badge">${sub.count} habilidades</span>
                </div>
            `).join('');
        }

        function openSub(catName, subName) {
            const cat = data.find(c => c.name === catName);
            if (!cat) return;
            const sub = cat.subcategories.find(s => s.name === subName);
            if (!sub) return;

            navStack.push({ title: subName, action: () => { showView('viewSkills'); renderSkillCards(sub.skills, document.getElementById('skillsGrid')); } });
            showView('viewSkills');
            renderSkillCards(sub.skills, document.getElementById('skillsGrid'));
            updateBreadcrumb();
            window.scrollTo(0, 0);
        }

        // Search
        document.getElementById('search').addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            if (term.length > 2) {
                const filtered = allSkills.filter(s =>
                    s.name.toLowerCase().includes(term) ||
                    s.description.toLowerCase().includes(term) ||
                    s.id.toLowerCase().includes(term)
                );
                navStack = [
                    { title: 'Categorías', action: () => { renderCategories(); navStack = [navStack[0]]; updateBreadcrumb(); } },
                    { title: `Búsqueda: "${e.target.value}"`, action: () => {} }
                ];
                showView('viewSkills');
                renderSkillCards(filtered, document.getElementById('skillsGrid'));
                updateBreadcrumb();
            } else if (term.length === 0) {
                navStack = [{ title: 'Categorías', action: renderCategories }];
                renderCategories();
                updateBreadcrumb();
            }
        });

        // Init
        navStack = [{ title: 'Categorías', action: renderCategories }];
        renderCategories();
    </script>
</body>
</html>
    """

    final_html = html_template.replace("%DATA%", json.dumps(categories_list, indent=2))
    final_html = final_html.replace("%ALL_SKILLS%", json.dumps(skills, indent=2))

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(final_html)

if __name__ == "__main__":
    data = get_skill_data()
    generate_html(data)
    print(f"Dashboard generado en {OUTPUT_FILE} con {len(data)} habilidades.")
