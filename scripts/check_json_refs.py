import os
import json

def collect_skill_ids(skills_dir):
    ids = set()
    for root, dirs, files in os.walk(skills_dir):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        if "SKILL.md" in files:
            rel = os.path.relpath(root, skills_dir)
            ids.add(rel)
    return ids

def check_json_references(base_path):
    skills_dir = os.path.join(base_path, 'skills')
    valid_skills = collect_skill_ids(skills_dir)
    
    data_dir = os.path.join(base_path, 'data')
    errors = []
    
    # Check bundles.json
    bundles_path = os.path.join(data_dir, 'bundles.json')
    if os.path.exists(bundles_path):
        with open(bundles_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for bid, bundle in data.get('bundles', {}).items():
                for slug in bundle.get('skills', []):
                    if slug not in valid_skills:
                        errors.append(f"bundles.json bundle '{bid}' -> missing skill: {slug}")
                        
    # Check workflows.json
    workflows_path = os.path.join(data_dir, 'workflows.json')
    if os.path.exists(workflows_path):
        with open(workflows_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for w in data.get('workflows', []):
                w_id = w.get('id', '?')
                for step in w.get('steps', []):
                    for slug in step.get('recommendedSkills', []):
                        if slug not in valid_skills:
                            errors.append(f"workflows.json workflow '{w_id}' -> missing skill: {slug}")
                            
    return errors

if __name__ == "__main__":
    repo_root = os.getcwd()
    errors = check_json_references(repo_root)
    if errors:
        for e in errors:
            print(e)
    else:
        print("No broken references in JSON data.")
