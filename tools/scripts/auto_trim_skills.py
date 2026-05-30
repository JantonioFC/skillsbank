import os
import re
import yaml

def trim_description(desc):
    if len(desc) <= 300:
        return desc
    # Intelligent trimming: find last space or punctuation under 297 characters
    truncated = desc[:297]
    # Try to find a space or period to trim neatly
    for char in ['. ', ', ', '; ', ' ']:
        idx = truncated.rfind(char)
        if idx > 200:
            return truncated[:idx] + "..."
    return truncated + "..."

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fm_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not fm_match:
        print(f"Skipping {path}: No frontmatter found")
        return
    
    fm_text = fm_match.group(1)
    try:
        # Load the YAML
        metadata = yaml.safe_load(fm_text) or {}
    except Exception as e:
        # If it fails to load, maybe because of unquoted colons (like harness-engineering)
        print(f"YAML Parse Error in {path}: {e}")
        # Try a regex-based fallback to extract/quote description
        match = re.search(r'^description:\s*(.*)$', fm_text, re.MULTILINE)
        if match:
            desc_val = match.group(1).strip()
            # If not quoted, wrap in double quotes
            if not (desc_val.startswith('"') and desc_val.endswith('"')) and not (desc_val.startswith("'") and desc_val.endswith("'")):
                # Escape double quotes inside
                escaped = desc_val.replace('"', '\\"')
                fm_text_fixed = fm_text.replace(match.group(0), f'description: "{escaped}"')
                try:
                    metadata = yaml.safe_load(fm_text_fixed) or {}
                    print(f"Successfully recovered {path} using regex pre-quoting!")
                except Exception as e2:
                    print(f"Could not recover {path}: {e2}")
                    return
            else:
                return
        else:
            return

    # Update description if it is present
    if "description" in metadata:
        orig_desc = metadata["description"]
        if isinstance(orig_desc, str):
            trimmed = trim_description(orig_desc)
            if trimmed != orig_desc or ":" in trimmed:
                metadata["description"] = trimmed
                # Serialize YAML back
                new_fm = yaml.safe_dump(metadata, default_flow_style=False, allow_unicode=True, sort_keys=False).strip()
                # Replace the old frontmatter with new frontmatter
                new_content = "---\n" + new_fm + "\n---" + content[fm_match.end():]
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Fixed description in {path} (length: {len(orig_desc)} -> {len(trimmed)})")
            else:
                # Even if not trimmed, let's re-serialize to ensure it's safely quoted if it has colons
                new_fm = yaml.safe_dump(metadata, default_flow_style=False, allow_unicode=True, sort_keys=False).strip()
                new_content = "---\n" + new_fm + "\n---" + content[fm_match.end():]
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Normalized frontmatter in {path}")

def main():
    skills_dir = 'skills'
    for root, dirs, files in os.walk(skills_dir):
        # Skip .disabled or hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        if "SKILL.md" in files:
            path = os.path.join(root, "SKILL.md")
            if os.path.islink(path):
                continue
            fix_file(path)

if __name__ == '__main__':
    main()
