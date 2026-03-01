
import os
import yaml
from pathlib import Path

SKILLS_DIR = Path("/home/juan/Escritorio/antigravity-awesome-skills/skills")

def fix_name_mismatch():
    count = 0
    for skill_path in SKILLS_DIR.iterdir():
        if not skill_path.is_dir(): continue
        skill_md = skill_path / "SKILL.md"
        if not skill_md.exists(): continue
        
        with open(skill_md, "r") as f:
            content = f.read()
            
        if not content.startswith("---"): continue
        
        parts = content.split("---", 2)
        if len(parts) < 3: continue
        
        fm_str = parts[1]
        try:
            fm = yaml.safe_load(fm_str) or {}
        except:
            continue
            
        if "name" in fm and fm["name"] != skill_path.name:
            print(f"Fixing name: {fm['name']} -> {skill_path.name}")
            fm["name"] = skill_path.name
            new_fm = yaml.dump(fm, sort_keys=False, allow_unicode=True)
            with open(skill_md, "w") as f:
                f.write("---\n" + new_fm + "---\n" + parts[2])
            count += 1
    return count

if __name__ == "__main__":
    c = fix_name_mismatch()
    print(f"Fixed {c} name mismatches.")
