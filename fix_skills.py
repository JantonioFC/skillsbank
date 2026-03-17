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

    # Extract YAML frontmatter
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not fm_match:
        print(f"No frontmatter in {filepath}")
        return

    fm_text = fm_match.group(1)
    body = content[fm_match.end():]

    try:
        data = yaml.safe_load(fm_text)
    except Exception as e:
        print(f"Error parsing YAML in {filepath}: {e}")
        return

    changes = False

    # Fix name to match folder
    folder_name = Path(filepath).parent.name
    if data.get('name') != folder_name:
        data['name'] = folder_name
        changes = True

    # Add default risk
    if 'risk' not in data:
        data['risk'] = 'unknown'
        changes = True

    # Add default source
    if 'source' not in data:
        data['source'] = 'community'
        changes = True

    # Fix 300 char description limit & Missing description
    description = data.get('description', '')
    if not description:
        description = folder_name.replace('-', ' ').capitalize()
        data['description'] = description
        changes = True
    elif len(description) > 300:
        data['description'] = description[:297] + "..."
        changes = True

    if changes:
        new_fm = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False).strip()
        new_content = f"---\n{new_fm}\n---\n"
        
        # Ensure ## When to Use exists
        if "## When to Use" not in body:
            # Try to insert it before the first section or at the end
            if body.strip():
                new_content += body.rstrip() + "\n\n## When to Use\n- Use this skill when you need for functional programming or specific domain tasks.\n"
            else:
                new_content += "## When to Use\n- Use this skill when you need to perform the target task.\n"
        else:
            new_content += body

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

skills_dir = 'skills'
fixed_count = 0
for root, dirs, files in os.walk(skills_dir):
    if 'SKILL.md' in files:
        if fix_skill_file(os.path.join(root, 'SKILL.md')):
            fixed_count += 1

print(f"Correcciones aplicadas a {fixed_count} archivos SKILL.md")
