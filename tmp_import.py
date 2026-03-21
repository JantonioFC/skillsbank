import subprocess
import os

def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode().strip()

# Obtener todos los remotos
remotes = run_cmd("git remote").splitlines()
remotes = [r for r in remotes if r not in ['origin', 'backup']]

imported_count = 0

for remote in remotes:
    print(f"\\nProcesando remoto: {remote}")
    # Determinar si la rama principal es main o master
    branch = f"{remote}/main"
    if subprocess.call(f"git rev-parse --verify {branch}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
        branch = f"{remote}/master"
        if subprocess.call(f"git rev-parse --verify {branch}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
            print(f"No se encontró rama principal para {remote}. Omitiendo.")
            continue
            
    # Listar directorios que contienen SKILL.md
    try:
        paths = run_cmd(f"git ls-tree -r --name-only {branch}").splitlines()
    except subprocess.CalledProcessError:
        continue
        
    skill_dirs = set()
    for p in paths:
        if p.endswith("SKILL.md"):
            dirname = os.path.dirname(p)
            # Ignoramos si SKILL.md está en la raíz
            if dirname:
                skill_dirs.add(dirname)
                
    for sdir in skill_dirs:
        skill_name = os.path.basename(sdir)
        target_dir = os.path.join('skills', skill_name)
        
        # Si la skill NO existe localmente, la importamos. 
        # (Para extraer updates de skills existentes podríamos verificar if target_dir exists,
        # pero para seguridad y evitar destruir cosas, extraemos/sobreescribimos con git archive).
        
        print(f"Importando skill: {skill_name} desde {branch}:{sdir}")
        os.makedirs(target_dir, exist_ok=True)
        # Extraer directorio desde git
        # Strip components depends on the depth of sdir
        strip_count = sdir.count('/') + 1
        cmd = f"git archive {branch} {sdir} | tar -x -C {target_dir} --strip-components={strip_count}"
        subprocess.call(cmd, shell=True)
        imported_count += 1

print(f"\\nProceso terminado. Se extrajeron {imported_count} carpetas de skills.")
