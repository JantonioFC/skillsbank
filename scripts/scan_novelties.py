import os
import subprocess
import json

def run_cmd(cmd, cwd=None):
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, cwd=cwd).decode().strip()
    except subprocess.CalledProcessError as e:
        return e.output.decode()

def main():
    if not os.path.exists('import_status.json'):
        print("Error: import_status.json not found.")
        return

    with open('import_status.json', 'r') as f:
        status = json.load(f)

    imported_skills = status.get('imported', [])
    if not imported_skills:
        print("No skills imported to scan.")
        return

    print(f"Scanning {len(imported_skills)} newly imported skills...")
    
    scan_results = {}
    
    # Path to the scanner venv and entry point
    scanner_dir = os.path.abspath('herramientas-seguridad')
    venv_python = os.path.join(scanner_dir, 'venv_new/bin/python3')
    
    for skill in imported_skills:
        skill_path = os.path.abspath(os.path.join('skills', skill))
        if not os.path.exists(skill_path):
            print(f"Skill path not found: {skill_path}")
            continue

        print(f"Scanning skill: {skill}...")
        # Run the scanner
        # Use --use-behavioral for deeper analysis
        cmd = f"PYTHONPATH={scanner_dir} {venv_python} -m skill_scanner.cli.cli scan {skill_path} --use-behavioral --format json"
        output = run_cmd(cmd)
        
        try:
            # The output might contain some logging before the JSON
            # Find the first '{' and last '}'
            start = output.find('{')
            end = output.rfind('}')
            if start != -1 and end != -1:
                json_str = output[start:end+1]
                result = json.loads(json_str)
                scan_results[skill] = result
            else:
                print(f"  Error: Could not find JSON in scanner output for {skill}")
                scan_results[skill] = {"error": "Invalid JSON output", "output": output}
        except Exception as e:
            print(f"  Error parsing result for {skill}: {e}")
            scan_results[skill] = {"error": str(e), "output": output}

    # Write summary report
    with open('novelties_security_scan.json', 'w') as f:
        json.dump(scan_results, f, indent=4)
    
    # Simple summary table
    print("\nSecurity Scan Summary:")
    print(f"{'Skill':<30} | {'Status':<10} | {'Max Severity':<12}")
    print("-" * 60)
    for skill, res in scan_results.items():
        status = res.get('status', 'ERROR')
        severity = res.get('max_severity', 'N/A')
        print(f"{skill[:30]:<30} | {status:<10} | {severity:<12}")

if __name__ == "__main__":
    main()
