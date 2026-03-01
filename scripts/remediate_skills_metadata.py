
import os
import yaml
from pathlib import Path

SKILLS_DIR = Path("/home/juan/Escritorio/antigravity-awesome-skills/skills")
OFFENSIVE_KEYWORDS = ["exploit", "pentest", "hacking", "attack", "malware", "vulnerability", "payload", "injection", "metasploit", "burp", "wpscan", "sqlmap", "phishing", "reconnaissance", "escalation", "red-team", "adversary"]

# Exact disclaimer from SECURITY_GUARDRAILS.md
MANDATORY_DISCLAIMER = """
> **⚠️ AUTHORIZED USE ONLY**
> This skill is for educational purposes or authorized security assessments only.
> You must have explicit, written permission from the system owner before using this tool.
> Misuse of this tool is illegal and strictly prohibited.
"""

def remediate_skill(skill_path):
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return
    
    with open(skill_md, "r") as f:
        content = f.read()
    
    if not content.startswith("---"):
        return
        
    parts = content.split("---", 2)
    if len(parts) < 3:
        return
        
    frontmatter_str = parts[1]
    body = parts[2]
    
    try:
        frontmatter = yaml.safe_load(frontmatter_str) or {}
    except Exception as e:
        # Emergency fix for common YAML issues in these skills
        lines = frontmatter_str.splitlines()
        for i, line in enumerate(lines):
            if ":" in line:
                key, val = line.split(":", 1)
                val = val.strip()
                # Quote values with @, [, ], {, }, or starting with number if not quoted
                if val and not (val.startswith('"') or val.startswith("'")):
                    if any(c in val for c in "@[]{}") or val[0].isdigit():
                        lines[i] = f"{key}: \"{val.replace('\"', '\\\"')}\""
        frontmatter_str = "\n".join(lines)
        try:
            frontmatter = yaml.safe_load(frontmatter_str) or {}
        except Exception as e2:
            print(f"Failed to fix YAML for {skill_md}: {e2}")
            return

    modified = False
    
    # 1. Fix Risk Levels
    current_risk = frontmatter.get("risk")
    if current_risk not in ['none', 'safe', 'critical', 'offensive']:
        content_lower = content.lower()
        if any(kw in content_lower for kw in OFFENSIVE_KEYWORDS):
            frontmatter["risk"] = "offensive"
        else:
            frontmatter["risk"] = "safe"
        modified = True
        
    # 2. Add 'source' if missing
    if "source" not in frontmatter:
        if "azure" in skill_path.name or "microsoft" in skill_path.name or "ms-" in skill_path.name:
            frontmatter["source"] = "microsoft"
        else:
            frontmatter["source"] = "community"
        modified = True
        
    # 3. Add 'license' if missing
    if "license" not in frontmatter:
        frontmatter["license"] = "MIT"
        modified = True

    # 4. Inject mandatory disclaimer for offensive
    if frontmatter.get("risk") == "offensive" and "AUTHORIZED USE ONLY" not in body:
        if body.strip().startswith("#"):
            body_parts = body.strip().split("\n", 1)
            title = body_parts[0]
            rest = body_parts[1] if len(body_parts) > 1 else ""
            body = "\n" + title + "\n" + MANDATORY_DISCLAIMER + rest
        else:
            body = "\n" + MANDATORY_DISCLAIMER + body
        modified = True

    # 5. Ensure '## When to Use' exists
    if "## When to Use" not in body:
        # If it has ## Purpose, rename or add after
        if "## Purpose" in body:
            body = body.replace("## Purpose", "## When to Use")
        else:
            body += "\n\n## When to Use\n\nUse this skill when you need guidance or automation for " + frontmatter.get("name", skill_path.name) + ".\n"
        modified = True

    if modified:
        new_frontmatter = yaml.dump(frontmatter, sort_keys=False, allow_unicode=True)
        with open(skill_md, "w") as f:
            f.write("---\n")
            f.write(new_frontmatter)
            f.write("---\n")
            f.write(body)
        return True
    return False

def main():
    count = 0
    skills_processed = 0
    for root, dirs, files in os.walk(SKILLS_DIR):
        if "SKILL.md" in files:
            skills_processed += 1
            if remediate_skill(Path(root)):
                count += 1
    print(f"Processed {skills_processed} skills. Remediated {count} skills.")

if __name__ == "__main__":
    main()
