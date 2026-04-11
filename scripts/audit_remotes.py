import os
import subprocess
import json

def run_command(cmd):
    try:
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        return None

def get_remote_branches():
    output = run_command(['git', 'branch', '-r'])
    if not output:
        return []
    return [line.strip() for line in output.split('\n')]

def get_skills_from_branch(branch):
    # Find all SKILL.md files recursively
    output = run_command(['git', 'ls-tree', '-r', '--name-only', branch])
    if not output:
        return []
    
    skills = []
    for line in output.split('\n'):
        if line.endswith('/SKILL.md'):
            # The skill name is the name of the parent directory
            skill_name = os.path.basename(os.path.dirname(line))
            if skill_name and skill_name not in ['scripts', 'skills']:
                skills.append(skill_name)
    return list(set(skills))

def main():
    print("Auditing remotes for new skills...")
    
    # Get local skills
    local_skills = set(os.listdir('skills')) if os.path.exists('skills') else set()
    print(f"Total local skills: {len(local_skills)}")

    # Get remotes
    remotes_output = run_command(['git', 'remote'])
    if not remotes_output:
        print("No remotes found.")
        return
    remotes = remotes_output.split('\n')

    all_remote_branches = get_remote_branches()
    
    report = {}

    for remote in remotes:
        if remote == 'origin': continue # Skip origin as it is likely our own
        
        # Try to find the main branch of the remote
        main_branch = None
        for b in [f"{remote}/main", f"{remote}/master"]:
            if any(b in line for line in all_remote_branches):
                main_branch = b
                break
        
        if not main_branch:
            # If no obvious main/master, just skip or look for something else
            continue

        print(f"Checking remote '{remote}' ({main_branch})...")
        remote_skills = get_skills_from_branch(main_branch)
        
        novelties = [s for s in remote_skills if s not in local_skills]
        if novelties:
            report[remote] = novelties
            print(f"  Found {len(novelties)} new skills.")

    # Output report
    if report:
        with open('remote_audit_report.json', 'w') as f:
            json.dump(report, f, indent=4)
        print("\nAudit complete. Results saved to 'remote_audit_report.json'.")
        
        print("\nSummary of Novelties:")
        for remote, skills in report.items():
            print(f"[{remote}]: {len(skills)} new skills")
            if len(skills) <= 10:
                for s in skills:
                    print(f"  - {s}")
            else:
                for s in skills[:10]:
                    print(f"  - {s}")
                print(f"  - ... and {len(skills) - 10} more.")
    else:
        print("\nNo new skills found across all remotes.")

if __name__ == "__main__":
    main()
