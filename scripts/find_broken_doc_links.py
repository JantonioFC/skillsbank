import os
import re

def find_broken_links(base_path):
    skills_dir = os.path.join(base_path, 'skills')
    docs_dir = os.path.join(base_path, 'docs')
    valid_skills = {d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))}
    
    broken = []
    
    # Common link patterns: ../../skills/slug/ or [slug](../../skills/slug/)
    pattern = re.compile(r'\]\((?:\.\./)*skills/([^/)]+)/?\)')
    
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    matches = pattern.findall(content)
                    for slug in matches:
                        if slug not in valid_skills:
                            broken.append((os.path.relpath(path, base_path), slug))
                            
    return broken

if __name__ == "__main__":
    repo_root = os.getcwd()
    broken_links = find_broken_links(repo_root)
    if broken_links:
        print("Found broken links in docs:")
        for path, slug in broken_links:
            print(f"{path} -> missing skill: {slug}")
    else:
        print("No broken skill links found in docs.")
