
import os
import yaml
from pathlib import Path
import re

SKILLS_DIR = Path("/home/juan/Escritorio/antigravity-awesome-skills/skills")

TARGET_SKILLS = [
    "seo-audit", "form-cro", "nodejs-best-practices", "content-creator", 
    "analytics-tracking", "schema-markup", "mcp-builder-ms", "context-compression", 
    "tailwind-patterns", "programmatic-seo", "page-cro"
]

def final_remediate(skill_name):
    skill_path = SKILLS_DIR / skill_name
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists(): return
    
    with open(skill_md, "r") as f:
        content = f.read()
    
    # 1. Force Level 2 for When to Use
    # If it's ### When to Use, make it ## When to Use
    content = content.replace("### When to Use", "## When to Use")
    
    # 2. Check if it's still missing at top-level
    if "## When to Use" not in content:
        # Prepend to body after frontmatter
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm = parts[1]
            body = parts[2].strip()
            # If it has ## Purpose, replace it
            if "## Purpose" in body:
                body = body.replace("## Purpose", "## When to Use")
            else:
                body = "## When to Use\n\nThis skill provides specialized guidance for " + skill_name + ".\n\n" + body
            content = "---" + fm + "---\n\n" + body
            
    with open(skill_md, "w") as f:
        f.write(content)

def main():
    for skill in TARGET_SKILLS:
        print(f"Fixing hierarchy for {skill}")
        final_remediate(skill)

if __name__ == "__main__":
    main()
