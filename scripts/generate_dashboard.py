import os
import json
import re

SKILLS_DIR = "skills"
SOURCES_FILE = "docs/SOURCES.json"
OUTPUT_FILE = "docs/DASHBOARD.html"

def get_skill_data():
    skills = []
    # Load sources for better categorization
    sources_data = {}
    if os.path.exists(SOURCES_FILE):
        with open(SOURCES_FILE, "r") as f:
            data = json.load(f)
            for repo in data.get("repos", []):
                sources_data[repo["author"].lower()] = {
                    "author": repo["author"],
                    "categories": repo["categories"]
                }

    for item in os.listdir(SKILLS_DIR):
        path = os.path.join(SKILLS_DIR, item)
        if not os.path.isdir(path):
            continue
            
        skill_file = os.path.join(path, "SKILL.md")
        if not os.path.exists(skill_file):
            continue

        try:
            with open(skill_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception:
            continue

        # Extract frontmatter
        name = item
        description = "Sin descripción disponible"
        source = "community"
        
        fm_match = re.search(r'^---(.*?)---', content, re.DOTALL)
        if fm_match:
            fm = fm_match.group(1)
            name_match = re.search(r'name:\s*(.*)', fm)
            if name_match: name = name_match.group(1).strip().strip('"')
            
            desc_match = re.search(r'description:\s*"(.*?)"', fm)
            if not desc_match:
                desc_match = re.search(r'description:\s*(.*)', fm)
            if desc_match: description = desc_match.group(1).strip().strip('"')
            
            src_match = re.search(r'source:\s*(.*)', fm)
            if src_match: source = src_match.group(1).strip().strip('"')

        # Clean up description (shorten if too long)
        if len(description) > 160:
            description = description[:157] + "..."

        # Inherit categories from source if possible
        categories = sources_data.get(source.lower(), {}).get("categories", ["General"])
        
        skills.append({
            "id": item,
            "name": name,
            "description": description,
            "source": source,
            "categories": categories
        })
    
    return sorted(skills, key=lambda x: x["name"])

def generate_html(skills):
    # CSS/JS embedded for a single-file portable dashboard
    html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Awesome Skills Dashboard</title>
    <style>
        :root {
            --bg: #0f172a;
            --card-bg: #1e293b;
            --text: #f8fafc;
            --text-muted: #94a3b8;
            --primary: #38bdf8;
            --accent: #818cf8;
        }
        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        header {
            text-align: center;
            margin-bottom: 40px;
        }
        h1 {
            font-size: 2.5rem;
            background: linear-gradient(to right, var(--primary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        .search-container {
            position: sticky;
            top: 10px;
            z-index: 100;
            margin-bottom: 30px;
        }
        #search {
            width: 100%;
            padding: 15px 25px;
            font-size: 1.1rem;
            border-radius: 50px;
            border: 2px solid var(--card-bg);
            background: #1e293bd9;
            color: #fff;
            backdrop-filter: blur(10px);
            outline: none;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            transition: border-color 0.3s;
        }
        #search:focus {
            border-color: var(--primary);
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }
        .card {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 20px;
            transition: transform 0.2s, box-shadow 0.2s;
            border: 1px solid #334155;
            display: flex;
            flex-direction: column;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.4);
            border-color: var(--primary);
        }
        .card h3 {
            margin-top: 0;
            font-size: 1.25rem;
            color: var(--primary);
        }
        .card p {
            font-size: 0.9rem;
            line-height: 1.5;
            color: var(--text-muted);
            flex-grow: 1;
        }
        .card .meta {
            margin-top: 15px;
            font-size: 0.75rem;
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }
        .badge {
            background: #334155;
            padding: 3px 8px;
            border-radius: 4px;
            color: var(--accent);
        }
        .source-badge {
            color: #fbbf24;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Awesome Skills Dashboard</h1>
            <p id="stats"></p>
        </header>
        
        <div class="search-container">
            <input type="text" id="search" placeholder="Busca entre 950+ habilidades por nombre, descripción o categoría...">
        </div>

        <div class="grid" id="grid">
            <!-- Cards go here -->
        </div>
    </div>

    <script>
        const skills = %DATA%;
        const grid = document.getElementById('grid');
        const search = document.getElementById('search');
        const stats = document.getElementById('stats');

        function render(items) {
            grid.innerHTML = items.map(s => `
                <div class="card">
                    <h3>${s.name}</h3>
                    <p>${s.description}</p>
                    <div class="meta">
                        <span class="badge source-badge">@${s.source}</span>
                        ${s.categories.map(c => `<span class="badge">${c}</span>`).join('')}
                    </div>
                </div>
            `).join('');
            stats.innerText = `Mostrando ${items.length} de ${skills.length} habilidades disponibles.`;
        }

        search.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            const filtered = skills.filter(s => 
                s.name.toLowerCase().includes(term) || 
                s.description.toLowerCase().includes(term) ||
                s.source.toLowerCase().includes(term) ||
                s.categories.some(c => c.toLowerCase().includes(term))
            );
            render(filtered);
        });

        render(skills);
    </script>
</body>
</html>
    """
    
    final_html = html_template.replace("%DATA%", json.dumps(skills, indent=2))
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(final_html)

if __name__ == "__main__":
    data = get_skill_data()
    generate_html(data)
    print(f"Dashboard generado con éxito en {OUTPUT_FILE} con {len(data)} habilidades.")
