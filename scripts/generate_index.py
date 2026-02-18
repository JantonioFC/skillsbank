import os
import json
import re

import yaml

def parse_frontmatter(content):
    """
    Parses YAML frontmatter, sanitizing unquoted values containing @.
    Handles single values and comma-separated lists by quoting the entire line.
    """
    fm_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not fm_match:
        return {}
    
    yaml_text = fm_match.group(1)
    
    # Process line by line to handle values containing @ and commas
    sanitized_lines = []
    for line in yaml_text.splitlines():
        # Match "key: value" (handles keys with dashes like 'package-name')
        match = re.match(r'^(\s*[\w-]+):\s*(.*)$', line)
        if match:
            key, val = match.groups()
            val_s = val.strip()
            # If value contains @ and isn't already quoted, wrap the whole string in double quotes
            if '@' in val_s and not (val_s.startswith('"') or val_s.startswith("'")):
                # Escape any existing double quotes within the value string
                safe_val = val_s.replace('"', '\\"')
                line = f'{key}: "{safe_val}"'
        sanitized_lines.append(line)
    
    sanitized_yaml = '\n'.join(sanitized_lines)
    
    try:
        return yaml.safe_load(sanitized_yaml) or {}
    except yaml.YAMLError as e:
        print(f"⚠️ YAML parsing error: {e}")
        return {}

CATEGORY_RULES = [
    ("security", ["security", "sast", "compliance", "privacy", "threat", "vulnerability",
                   "owasp", "pci", "gdpr", "secrets", "risk", "malware", "forensics",
                   "attack", "incident", "auth", "mtls", "zero", "trust", "pentest",
                   "penetration", "exploit", "xss", "injection", "hacking"]),
    ("infrastructure", ["kubernetes", "k8s", "helm", "terraform", "cloud", "network",
                         "devops", "gitops", "prometheus", "grafana", "observability",
                         "monitoring", "logging", "tracing", "deployment", "istio",
                         "linkerd", "mesh", "slo", "sre", "oncall", "pipeline",
                         "cicd", "ci", "cd", "kafka", "docker", "aws", "azure", "gcp"]),
    ("data-ai", ["data", "database", "db", "sql", "postgres", "mysql", "analytics",
                  "etl", "warehouse", "dbt", "ml", "ai", "llm", "rag", "vector",
                  "embedding", "spark", "airflow", "cdc"]),
    ("development", ["python", "javascript", "typescript", "java", "golang", "go",
                      "rust", "csharp", "dotnet", "php", "ruby", "node", "react",
                      "frontend", "backend", "mobile", "ios", "android", "flutter",
                      "fastapi", "django", "nextjs", "vue", "api", "swift", "scala",
                      "haskell", "elixir", "laravel", "angular", "springboot", "fp-ts",
                      "functional"]),
    ("architecture", ["architecture", "c4", "microservices", "event", "cqrs", "saga",
                       "domain", "ddd", "adr", "architect"]),
    ("testing", ["testing", "tdd", "unit", "e2e", "qa", "test"]),
    ("business", ["business", "market", "sales", "finance", "startup", "legal", "hr",
                   "product", "customer", "seo", "marketing", "kpi", "contract",
                   "employment", "email", "content", "brand", "pricing", "ceo", "cto",
                   "revenue", "analyst"]),
    ("workflow", ["workflow", "orchestration", "conductor", "automation", "process",
                   "collaboration", "agent"]),
]


SUBCATEGORY_RULES = {
    "infrastructure": [
        ("containers", {
            "tokens": {"kubernetes", "k8s", "helm", "docker", "container", "istio"},
            "prefixes": [],
        }),
        ("observability", {
            "tokens": {"observability", "monitoring", "tracing", "prometheus", "grafana", "diagnostics"},
            "prefixes": [],
        }),
        ("messaging", {
            "tokens": {"servicebus", "eventhub", "eventgrid", "kafka", "queue", "messaging"},
            "prefixes": [],
        }),
        ("ci-cd", {
            "tokens": {"cicd", "pipeline", "deploy", "gitops"},
            "prefixes": ["github-actions", "gitlab-ci"],
        }),
        ("cloud-services", {
            "tokens": {"aws", "gcp", "serverless", "azd"},
            "prefixes": ["azure-mgmt", "azure-identity", "azure-resource"],
        }),
        # fallback — must be last
        ("infra-general", {
            "tokens": set(),
            "prefixes": [],
        }),
    ],
    "general": [
        ("game-dev", {
            "tokens": {"game", "games", "unity", "vr", "ar", "threejs"},
            "prefixes": [],
        }),
        ("code-quality", {
            "tokens": {"review", "refactor", "lint", "debug", "standards", "tech-debt"},
            "prefixes": ["clean-code"],
        }),
        ("docs-formats", {
            "tokens": {"docx", "pptx", "xlsx", "pdf", "wiki", "readme", "changelog"},
            "prefixes": [],
        }),
        ("design-ux", {
            "tokens": {"design", "ux", "ui", "brand", "visual", "canvas", "carousel", "thumbnail"},
            "prefixes": [],
        }),
        ("agent-tools", {
            "tokens": {"context", "memory", "planning", "skill", "eval", "superpowers", "dispatching"},
            "prefixes": [],
        }),
        # fallback — must be last
        ("general-misc", {
            "tokens": set(),
            "prefixes": [],
        }),
    ],
    "development": [
        ("python", {
            "tokens": {"python", "django", "fastapi", "pydantic"},
            "prefixes": [],
        }),
        ("frontend", {
            "tokens": {"react", "angular", "vue", "nextjs", "frontend", "responsive", "zustand"},
            "prefixes": [],
        }),
        ("fp-ts", {
            "tokens": {"functional"},
            "prefixes": ["fp-"],
        }),
        ("mobile", {
            "tokens": {"ios", "android", "flutter", "mobile", "expo", "swiftui", "swift"},
            "prefixes": [],
        }),
        ("azure-sdk", {
            "tokens": set(),
            "prefixes": ["azure-communication", "azure-storage", "azure-keyvault",
                         "azure-ai", "azure-cosmos", "azure-monitor", "azure-servicebus",
                         "azure-eventhub", "azure-eventgrid", "azure-search",
                         "azure-appconfiguration", "azure-data", "azure-security",
                         "azure-postgres", "azure-containerregistry", "azure-messaging",
                         "azure-web"],
        }),
        # fallback — must be last
        ("dev-general", {
            "tokens": set(),
            "prefixes": [],
        }),
    ],
}


def detect_subcategory(skill_id, name, description, category):
    """Detect subcategory using keyword + prefix matching. Returns None for categories without rules."""
    rules = SUBCATEGORY_RULES.get(category)
    if not rules:
        return None

    haystack = set()
    for text in [skill_id, name, description]:
        if text:
            haystack.update(re.split(r'[\s\-_/]+', text.lower()))

    for sub_name, rule in rules:
        # prefix match on skill_id
        for prefix in rule["prefixes"]:
            if skill_id.startswith(prefix):
                return sub_name
        # token match
        if rule["tokens"] and rule["tokens"] & haystack:
            return sub_name
        # fallback: entry with no tokens and no prefixes acts as catch-all
        if not rule["tokens"] and not rule["prefixes"]:
            return sub_name

    return None


def detect_category(skill_id, name, description):
    """Detect category using keyword matching (mirrors build-catalog.js logic)."""
    haystack = set()
    for text in [skill_id, name, description]:
        if text:
            haystack.update(re.split(r'[\s\-_/]+', text.lower()))

    for cat_name, keywords in CATEGORY_RULES:
        for keyword in keywords:
            if keyword in haystack:
                return cat_name

    return "general"


def generate_index(skills_dir, output_file):
    print(f"🏗️ Generating index from: {skills_dir}")
    skills = []

    for root, dirs, files in os.walk(skills_dir):
        # Skip .disabled or hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        if "SKILL.md" in files:
            skill_path = os.path.join(root, "SKILL.md")
            dir_name = os.path.basename(root)
            parent_dir = os.path.basename(os.path.dirname(root))

            # Use parent dir as category hint if nested, otherwise detect later
            folder_category = parent_dir if parent_dir != "skills" else None

            # Default values
            skill_info = {
                "id": dir_name,
                "path": os.path.relpath(root, os.path.dirname(skills_dir)),
                "category": "general",
                "subcategory": None,
                "name": dir_name.replace("-", " ").title(),
                "description": "",
                "risk": "unknown",
                "source": "unknown"
            }
            
            try:
                with open(skill_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"⚠️ Error reading {skill_path}: {e}")
                continue

            # Parse Metadata
            metadata = parse_frontmatter(content)
            
            # Merge Metadata
            if "name" in metadata: skill_info["name"] = metadata["name"]
            if "description" in metadata: skill_info["description"] = metadata["description"]
            if "risk" in metadata: skill_info["risk"] = metadata["risk"]
            if "source" in metadata: skill_info["source"] = metadata["source"]
            
            # Fallback for description if missing in frontmatter (legacy support)
            if not skill_info["description"]:
                body = content
                fm_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
                if fm_match:
                    body = content[fm_match.end():].strip()
                
                # Simple extraction of first non-header paragraph
                lines = body.split('\n')
                desc_lines = []
                for line in lines:
                    if line.startswith('#') or not line.strip():
                        if desc_lines: break
                        continue
                    desc_lines.append(line.strip())
                
                if desc_lines:
                    skill_info["description"] = " ".join(desc_lines)[:250].strip()

            # Assign category: use folder parent if it's a known category, otherwise detect
            known_categories = {cat for cat, _ in CATEGORY_RULES}
            if folder_category and folder_category in known_categories:
                skill_info["category"] = folder_category
            else:
                skill_info["category"] = detect_category(
                    skill_info["id"], skill_info["name"], skill_info["description"]
                )

            # Assign subcategory based on category
            skill_info["subcategory"] = detect_subcategory(
                skill_info["id"], skill_info["name"], skill_info["description"],
                skill_info["category"]
            )

            skills.append(skill_info)

    # Sort validation: by name
    skills.sort(key=lambda x: (x["name"].lower(), x["id"].lower()))

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(skills, f, indent=2)
    
    print(f"✅ Generated rich index with {len(skills)} skills at: {output_file}")
    return skills

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skills_path = os.path.join(base_dir, "skills")
    output_path = os.path.join(base_dir, "skills_index.json")
    generate_index(skills_path, output_path)
