#!/usr/bin/env python3
import sys
import re
from pathlib import Path

def get_bundle_skills(bundle_queries):
    bundles_path = Path(__file__).parent.parent.parent / "docs" / "users" / "bundles.md"
    if not bundles_path.exists():
        print(f"Error: {bundles_path} not found", file=sys.stderr)
        return []

    content = bundles_path.read_text(encoding="utf-8")
    
    # Split by bundle headers
    sections = re.split(r'\n### ', content)
    
    selected_skills = set()
    
    for query in bundle_queries:
        query = query.lower().strip('"\'')
        found = False
        for section in sections:
            header_line = section.split('\n')[0].lower()
            if query in header_line:
                found = True
                # Extract skill names from bullet points: - [`skill-name`](../../skills/skill-name/)
                skills = re.findall(r'- \[`([^`]+)`\]', section)
                selected_skills.update(skills)
        
        if not found:
            # If query not found in any header, check if it's a skill name itself
            # (Just in case the user passed a skill name instead of a bundle)
            selected_skills.add(query)

    return sorted(list(selected_skills))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Default to Essentials if no query
        queries = ["essentials"]
    else:
        queries = sys.argv[1:]
    
    skills = get_bundle_skills(queries)
    if skills:
        print(" ".join(skills))
