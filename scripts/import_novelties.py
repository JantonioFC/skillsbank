import os
import subprocess
import json

def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode().strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{cmd}': {e.output.decode()}")
        return None

def main():
    if not os.path.exists('remote_audit_report.json'):
        print("Error: remote_audit_report.json not found.")
        return

    with open('remote_audit_report.json', 'r') as f:
        report = json.load(f)

    imported_skills = []
    failed_imports = []

    for remote, skills in report.items():
        print(f"\nProcessing remote: {remote}")
        # Identify main branch
        branch = f"{remote}/main"
        if run_cmd(f"git rev-parse --verify {branch}") is None:
            branch = f"{remote}/master"
            if run_cmd(f"git rev-parse --verify {branch}") is None:
                print(f"Could not find main/master branch for {remote}. Skipping.")
                continue

        # Get all file paths in the branch to find the skill directory
        branch_files = run_cmd(f"git ls-tree -r --name-only {branch}").splitlines()

        for skill_name in skills:
            # Find the actual path of the skill in the remote
            skill_source_path = None
            # Be very specific to find the directory that CONTAINS SKILL.md and ends with /skill_name
            for p in branch_files:
                if p.endswith(f"/{skill_name}/SKILL.md") or p == f"{skill_name}/SKILL.md":
                    skill_source_path = os.path.dirname(p)
                    break
            
            if not skill_source_path and skill_source_path != '':
                print(f"Could not find source path for skill: {skill_name}. Skipping.")
                failed_imports.append(f"{remote}:{skill_name}")
                continue

            target_dir = os.path.join('skills', skill_name)
            if os.path.exists(target_dir):
                print(f"Skill '{skill_name}' already exists locally. Skipping.")
                continue

            print(f"Importing skill: {skill_name} from {branch}:{skill_source_path}")
            os.makedirs(target_dir, exist_ok=True)
            
            # Use git archive to extract the directory
            strip_count = skill_source_path.count('/') + 1
            cmd = f"git archive {branch} {skill_source_path} | tar -x -C {target_dir} --strip-components={strip_count}"
            subprocess.call(cmd, shell=True)
            imported_skills.append(skill_name)

    print(f"\nImport process finished.")
    print(f"Successfully imported: {len(imported_skills)} skills.")
    if failed_imports:
        print(f"Failed to import: {len(failed_imports)} skills.")
        for f in failed_imports:
            print(f"  - {f}")

    # Write status to file
    with open('import_status.json', 'w') as f:
        json.dump({
            "imported": imported_skills,
            "failed": failed_imports
        }, f, indent=4)

if __name__ == "__main__":
    main()
