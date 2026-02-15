import os
import json
import re

SKILLS_DIR = "skills"
SOURCES_FILE = "docs/SOURCES.json"
OUTPUT_FILE = "docs/DASHBOARD.html"

# Mapeo de categorías maestras en castellano
CATEGORY_MAPPING = {
    "Nube e Infraestructura": ["cloud", "azure", "aws", "infrastructure", "server", "deploy"],
    "Desarrollo Frontend": ["frontend", "react", "nextjs", "css", "html", "javascript", "tailwind", "ui", "ux"],
    "Inteligencia Artificial": ["ai", "artificial", "intelligence", "gpt", "model", "prompt", "inference", "llm", "vision"],
    "Automatización": ["automation", "workflow", "process", "tool", "agent"],
    "Navegación Web": ["browser", "web", "navigation", "crawler", "chrome"],
    "Seguridad y Auditoría": ["security", "audit", "security", "protect", "hacker", "vulnerability"],
    "Desarrollo Backend": ["backend", "dotnet", "api", "database", "sql", "server", "architecture", "node"],
    "Multimedia y Contenido": ["video", "image", "audio", "multimedia", "design", "creative", "youtube"],
    "Ciencia de Datos": ["data", "science", "analysis", "statistics", "math"],
    "Productividad": ["writing", "blog", "office", "docx", "pdf", "pptx", "excel"]
}

# Traducciones heurísticas para descripciones
TRANSLATION_RULES = [
    (r'Use for:', 'Usar para:'),
    (r'Covers:', 'Incluye:'),
    (r'Triggers:', 'Activadores:'),
    (r'How to', 'Cómo'),
    (r'Best practices', 'Mejores prácticas'),
    (r'Management', 'Gestión'),
    (r'Optimization', 'Optimización'),
    (r'Implementation', 'Implementación'),
    (r'Integration', 'Integración'),
    (r'Creation', 'Creación'),
    (r'Analysis', 'Análisis'),
    (r'Testing', 'Pruebas'),
    (r'patterns', 'patrones'),
    (r'guidelines', 'guías'),
    (r'framework', 'marco de trabajo'),
    (r'development', 'desarrollo'),
    (r'Skill', 'Habilidad')
]

def translate_text(text):
    if not text: return "Sin descripción"
    for pattern, replacement in TRANSLATION_RULES:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text

def classify_skill(name, desc, tags):
    full_text = f"{name} {desc} {' '.join(tags)}".lower()
    scores = {}
    for cat, keywords in CATEGORY_MAPPING.items():
        score = 0
        for kw in keywords:
            if kw in full_text:
                score += 1
        scores[cat] = score
    
    # Get highest score category, or General
    best_cat = max(scores, key=scores.get)
    if scores[best_cat] == 0:
        return "Comunidad y Otros"
    return best_cat

def get_skill_data():
    skills = []
    for item in os.listdir(SKILLS_DIR):
        path = os.path.join(SKILLS_DIR, item)
        if not os.path.isdir(path): continue
        skill_file = os.path.join(path, "SKILL.md")
        if not os.path.exists(skill_file): continue

        try:
            with open(skill_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except: continue

        name = item
        description = ""
        source = "community"
        tags = []
        
        fm_match = re.search(r'^---(.*?)---', content, re.DOTALL)
        if fm_match:
            fm = fm_match.group(1)
            name_match = re.search(r'name:\s*(.*)', fm)
            if name_match: name = name_match.group(1).strip().strip('"')
            desc_match = re.search(r'description:\s*"(.*?)"', fm)
            if not desc_match: desc_match = re.search(r'description:\s*(.*)', fm)
            if desc_match: description = desc_match.group(1).strip().strip('"')
            src_match = re.search(r'source:\s*(.*)', fm)
            if src_match: source = src_match.group(1).strip().strip('"')
            
            # Simple tag extraction from description triggers if present
            if "Triggers:" in description:
                tags = description.split("Triggers:")[1].split(",")

        # Clasificación inteligente
        category = classify_skill(name, description, tags)

        # Traducir descripción
        description = translate_text(description)
        if len(description) > 160: description = description[:157] + "..."
        
        skills.append({
            "id": item,
            "name": name,
            "description": description,
            "source": source,
            "category": category
        })
    
    return sorted(skills, key=lambda x: x["name"])

def generate_html(skills):
    # Agrupar por categoría
    categories_dict = {}
    for s in skills:
        c = s["category"]
        if c not in categories_dict:
            categories_dict[c] = []
        categories_dict[c].append(s)

    categories_list = []
    for cat, members in categories_dict.items():
        categories_list.append({
            "name": cat,
            "count": len(members),
            "skills": members
        })
    categories_list = sorted(categories_list, key=lambda x: x["name"])

    html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Awesome Skills - Dashboard Visual</title>
    <style>
        :root {
            --bg: #0d1117;
            --card-bg: #161b22;
            --card-hover: #21262d;
            --text: #c9d1d9;
            --text-bright: #f0f6fc;
            --primary: #58a6ff;
            --accent: #d2a8ff;
            --border: #30363d;
        }
        body { font-family: -apple-system, sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 0; }
        header { background: #161b22; padding: 20px 40px; border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 20px; }
        header h1 { margin: 0; font-size: 1.5rem; color: var(--primary); }
        .back-btn { background: #21262d; border: 1px solid var(--border); color: var(--text); padding: 8px 16px; border-radius: 6px; cursor: pointer; display: none; }
        .container { max-width: 1200px; margin: 40px auto; padding: 0 20px; }
        
        .search-bar { margin-bottom: 30px; }
        #search { width: 100%; max-width: 500px; padding: 12px; border-radius: 6px; border: 1px solid var(--border); background: var(--card-bg); color: #fff; }

        .cat-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
        .cat-card { background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; padding: 25px; cursor: pointer; transition: 0.2s; text-align: left; }
        .cat-card:hover { border-color: var(--accent); background: var(--card-hover); }
        .cat-card h2 { margin: 0; color: var(--text-bright); font-size: 1.3rem; }
        .cat-card .badge { display: inline-block; margin-top: 10px; background: #23863622; color: #3fb950; padding: 2px 8px; border-radius: 20px; font-size: 0.8rem; }

        .skills-grid { display: none; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
        .skill-item { background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; padding: 20px; }
        .skill-item h3 { margin: 0 0 10px 0; color: var(--primary); }
        .skill-item p { font-size: 0.9rem; line-height: 1.4; color: #8b949e; }
        .skill-item .source { margin-top: 15px; font-size: 0.75rem; color: var(--accent); font-weight: bold; }
    </style>
</head>
<body>
    <header>
        <button id="backBtn" class="back-btn" onclick="back()">← Categorías</button>
        <h1>Awesome Skills Dashboard</h1>
    </header>

    <div class="container">
        <div class="search-bar">
            <input type="text" id="search" placeholder="Busca skills en castellano...">
        </div>

        <div id="viewCategories" class="cat-grid"></div>
        
        <div id="viewSkills" style="display:none">
            <h2 id="catTitle" style="color: var(--accent); margin-bottom: 25px;"></h2>
            <div id="skillsGrid" class="skills-grid" style="display:grid"></div>
        </div>
    </div>

    <script>
        const data = %DATA%;
        const allSkills = %ALL_SKILLS%;
        
        function renderCats() {
            const grid = document.getElementById('viewCategories');
            grid.innerHTML = data.map(c => `
                <div class="cat-card" onclick="openCat('${c.name}')">
                    <h2>${c.name}</h2>
                    <span class="badge">${c.count} Skills</span>
                </div>
            `).join('');
        }

        function openCat(name) {
            const cat = data.find(c => c.name === name);
            document.getElementById('catTitle').innerText = name;
            const grid = document.getElementById('skillsGrid');
            grid.innerHTML = cat.skills.map(s => `
                <div class="skill-item">
                    <h3>${s.name}</h3>
                    <p>${s.description}</p>
                    <div class="source">@${s.source}</div>
                </div>
            `).join('');
            
            document.getElementById('viewCategories').style.display = 'none';
            document.getElementById('viewSkills').style.display = 'block';
            document.getElementById('backBtn').style.display = 'block';
            window.scrollTo(0, 0);
        }

        function back() {
            document.getElementById('viewCategories').style.display = 'grid';
            document.getElementById('viewSkills').style.display = 'none';
            document.getElementById('backBtn').style.display = 'none';
            document.getElementById('search').value = '';
        }

        document.getElementById('search').addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            if (term.length > 2) {
                document.getElementById('viewCategories').style.display = 'none';
                document.getElementById('viewSkills').style.display = 'block';
                document.getElementById('backBtn').style.display = 'block';
                document.getElementById('catTitle').innerText = `Búsqueda: "${term}"`;
                
                const filtered = allSkills.filter(s => 
                    s.name.toLowerCase().includes(term) || 
                    s.description.toLowerCase().includes(term)
                );
                
                const grid = document.getElementById('skillsGrid');
                grid.innerHTML = filtered.map(s => `
                    <div class="skill-item">
                        <h3>${s.name}</h3>
                        <p>${s.description}</p>
                        <div class="source">@${s.source}</div>
                    </div>
                `).join('');
            } else if (term.length === 0) {
                back();
            }
        });

        renderCats();
    </script>
</body>
</html>
    """
    
    final_html = html_template.replace("%DATA%", json.dumps(categories_list, indent=2))
    final_html = final_html.replace("%ALL_SKILLS%", json.dumps(skills, indent=2))
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(final_html)

if __name__ == "__main__":
    data = get_skill_data()
    generate_html(data)
    print(f"Dashboard Inteligente generado en {OUTPUT_FILE} con {len(data)} habilidades.")
