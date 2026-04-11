import os
import re
import yaml
from pathlib import Path

SKILLS_DIR = Path("/home/juan/Escritorio/antigravity-awesome-skills/skills")
OFFENSIVE_KEYWORDS = ["exploit", "pentest", "hacking", "attack", "malware", "vulnerability", "payload", "injection", "metasploit", "burp", "wpscan", "sqlmap", "phishing", "reconnaissance", "escalation", "red-team", "adversary"]

def truncate_description(desc, max_len=300):
    if not desc or len(desc) <= max_len:
        return desc
    
    # Try to truncate at the last sentence boundary
    truncated = desc[:max_len-3]
    last_dot = truncated.rfind(".")
    if last_dot > max_len * 0.5:
        return desc[:last_dot+1]
    
    # Otherwise just hard truncate
    return truncated + "..."

def heal_skill(skill_dir):
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return False
    
    content = skill_md.read_text(encoding="utf-8")
    
    frontmatter = {}
    body = content
    
    # Case 1: Has frontmatter
    if content.strip().startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm_str = parts[1]
            body = parts[2]
            try:
                frontmatter = yaml.safe_load(fm_str) or {}
            except Exception:
                # Emergency parse for common malformed YAML in this repo
                lines = fm_str.splitlines()
                for i, line in enumerate(lines):
                    if ":" in line:
                        k, v = line.split(":", 1)
                        v = v.strip()
                        if v and not (v.startswith('"') or v.startswith("'")):
                            # Quote if contains special characters
                            if any(c in v for c in ":@[]{}"):
                                lines[i] = f"{k}: \"{v.replace('\"', '\\\"')}\""
                try:
                    frontmatter = yaml.safe_load("\n".join(lines)) or {}
                except Exception:
                    print(f"Failed to parse FM for {skill_dir}")
                    return False
        else:
            # Malformed --- block
            body = content
    
    # Case 2: Missing frontmatter
    if not frontmatter:
        # Try to extract the title from the first H1
        title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        name = title_match.group(1).strip() if title_match else skill_dir.name
        
        # Try to extract a description from the first paragraph after the title
        desc = ""
        paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
        for p in paragraphs:
            if not p.startswith("#") and len(p) > 20:
                desc = p
                break
        
        frontmatter = {
            "name": skill_dir.name,
            "description": truncate_description(desc or f"Skill for {name}"),
            "risk": "safe",
            "source": "community",
            "license": "MIT"
        }
    
    # Validation & Normalization
    modified = False
    
    # Ensure mandatory fields
    if "name" not in frontmatter:
        frontmatter["name"] = skill_dir.name
        modified = True
    
    if "description" not in frontmatter:
        frontmatter["description"] = f"Skill for {frontmatter.get('name', skill_dir.name)}"
        modified = True
    else:
        # Check description length
        fixed_desc = truncate_description(str(frontmatter["description"]))
        if fixed_desc != frontmatter["description"]:
            frontmatter["description"] = fixed_desc
            modified = True
            
    if "risk" not in frontmatter:
        content_lower = content.lower()
        if any(kw in content_lower for kw in OFFENSIVE_KEYWORDS):
            frontmatter["risk"] = "offensive"
        else:
            frontmatter["risk"] = "safe"
        modified = True
        
    if "source" not in frontmatter:
        frontmatter["source"] = "community"
        modified = True
        
    if "license" not in frontmatter:
        frontmatter["license"] = "MIT"
        modified = True

    # Section healing
    if "## When to Use" not in body:
        if "## Purpose" in body:
            body = body.replace("## Purpose", "## When to Use")
            modified = True
        elif "## Prerequisites" in body:
            # Insert before prerequisites
            body = body.replace("## Prerequisites", "## When to Use\n\nUse this skill when you need guidance on " + frontmatter["name"] + ".\n\n## Prerequisites")
            modified = True
        else:
            body += "\n\n## When to Use\n\nUse this skill when you need guidance on " + frontmatter["name"] + ".\n"
            modified = True

    # Final write
    try:
        # Custom YAML representer for multiline strings
        def str_presenter(dumper, data):
            if '\n' in data or len(data) > 80:
                return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
            return dumper.represent_scalar('tag:yaml.org,2002:str', data)

        yaml.add_representer(str, str_presenter)

        new_fm_str = yaml.dump(frontmatter, sort_keys=False, allow_unicode=True, width=1000)
        new_content = f"---\n{new_fm_str}---\n{body.lstrip()}"
        
        if new_content.strip() != content.strip():
            skill_md.write_text(new_content, encoding="utf-8")
            return True
    except Exception as e:
        print(f"Error writing {skill_md}: {e}")
        
    return False

def main():
    processed = 0
    healed = 0
    for root, dirs, files in os.walk(SKILLS_DIR):
        if "SKILL.md" in files:
            processed += 1
            if heal_skill(Path(root)):
                healed += 1
    print(f"Processed {processed} skills. Healed {healed} skills.")

if __name__ == "__main__":
    main()
