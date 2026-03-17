import os
import re
from pathlib import Path
import yaml

def fix_skill_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return

    parent_dir = filepath.parent.name

    match = re.search(r'^---\n(.*?)\n---', content, flags=re.DOTALL)
    if match:
        frontmatter = match.group(1)
        
        try:
            metadata = yaml.safe_load(frontmatter) or {}
        except yaml.YAMLError:
            metadata = {}

        metadata['name'] = parent_dir
        if 'risk' not in metadata:
            metadata['risk'] = 'unknown'
        if 'source' not in metadata:
            metadata['source'] = 'community'
            
        desc = metadata.get('description', '')
        if isinstance(desc, str) and len(desc) > 295:
            metadata['description'] = desc[:290] + "..."
            
        new_frontmatter = yaml.dump(metadata, default_flow_style=False, sort_keys=False, allow_unicode=True)
        content = "---\n" + new_frontmatter + "---\n" + content[match.end():]
    else:
        new_frontmatter = f"---\nname: {parent_dir}\nrisk: unknown\nsource: community\ndescription: Community provided skill\n---\n\n"
        content = new_frontmatter + content
        
    if "## When to Use" not in content and "# When to Use" not in content and "When to Use" not in content:
        content = content.rstrip() + "\n\n## When to Use\nThis skill is applicable to execute the workflow or actions described in the overview.\n"
        
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"Error writing {filepath}: {e}")

if __name__ == "__main__":
    skills_dir = Path('/home/juan/Escritorio/antigravity-awesome-skills/skills')
    for skill_file in skills_dir.rglob('SKILL.md'):
        fix_skill_file(skill_file)
    print("Correcciones aplicadas a todos los SKILL.md")
