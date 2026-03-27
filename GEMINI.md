# GEMINI.md — Reglas del proyecto antigravity-awesome-skills

## 🔴 REGLAS INVIOLABLES

### Push de Git
**NUNCA** hacer push a ningún remoto excepto `backup` (skillsbank).

```bash
# ✅ CORRECTO — único remoto permitido
git push backup main
git push backup main --force

# ❌ PROHIBIDO — bajo ninguna circunstancia
git push origin main
git push <cualquier-otro-remoto> main
```

**Remotos configurados:**
- `backup` = `https://github.com/JantonioFC/skillsbank.git` → **ÚNICO destino de push**
- `origin` = `https://github.com/sickn33/antigravity-awesome-skills.git` → solo lectura / fetch

---

## Estructura del proyecto

- `skills/` — 1,977+ skills individuales (cada una con `SKILL.md`)
- `.github/workflows/` — CI/CD (pages.yml = Vite web app, jekyll desactivado)
- `scripts/` — utilidades de mantenimiento
- `fix_skills.py` — normaliza frontmatter de SKILL.md
- `apps/web-app/` — app Vite para GitHub Pages

## Comandos frecuentes

```bash
# Normalizar frontmatter de skills recién importadas
python3 fix_skills.py

# Commit y push estándar
git add skills/
git commit -m "feat/fix: descripción"
git push backup main
```
