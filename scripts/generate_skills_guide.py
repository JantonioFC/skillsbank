#!/usr/bin/env python3
"""Generate SKILLS_GUIDE.md from all skills in skills/ directory.
Handles: real SKILL.md, broken symlinks (via catalog.json fallback), meta dirs.
"""
import os
import re
import json
import yaml
from datetime import date
from pathlib import Path
from collections import defaultdict

SKILLS_DIR = Path("/home/juan/Escritorio/antigravity-awesome-skills/skills")
CATALOG_JSON = Path("/home/juan/Escritorio/antigravity-awesome-skills/data/catalog.json")
OUTPUT = Path("/home/juan/Escritorio/antigravity-awesome-skills/SKILLS_GUIDE.md")

META_DIRS = {'README', 'TEMPLATE', '__pycache__', 'SPDD', 'examples', 'references'}

WHEN_PATTERN = re.compile(r'^##\s+When\s+to\s+Use.*?$', re.IGNORECASE | re.MULTILINE)
NEXT_SECTION = re.compile(r'^##\s+', re.MULTILINE)


# ── helpers ────────────────────────────────────────────────────────────────────

def parse_frontmatter(content):
    if not content.startswith('---'):
        return {}, content
    end = content.find('---', 3)
    if end == -1:
        return {}, content
    try:
        fm = yaml.safe_load(content[3:end]) or {}
    except Exception:
        fm = {}
    return fm, content[end + 3:]


def extract_when_to_use(body):
    m = WHEN_PATTERN.search(body)
    if not m:
        return None
    rest = body[m.end():]
    nxt = NEXT_SECTION.search(rest)
    section = rest[:nxt.start()].strip() if nxt else rest.strip()
    if len(section) > 600:
        section = section[:600].rsplit('\n', 1)[0] + '\n_[...]_'
    return section or None


def load_catalog_index():
    """Build a name→entry dict from catalog.json for fallback lookups."""
    if not CATALOG_JSON.exists():
        return {}
    with open(CATALOG_JSON, encoding='utf-8') as f:
        data = json.load(f)
    index = {}
    for s in data.get('skills', []):
        name = s.get('name') or s['id'].split('/')[-1]
        if name not in index:   # keep first occurrence
            index[name] = s
    return index


# ── skill collectors ───────────────────────────────────────────────────────────

def read_real_skill(skill_dir):
    """Read a skill whose SKILL.md exists and is readable."""
    content = (skill_dir / 'SKILL.md').read_text(encoding='utf-8', errors='replace')
    fm, body = parse_frontmatter(content)
    return {
        'name':        fm.get('name') or skill_dir.name,
        'dir':         skill_dir.name,
        'description': fm.get('description') or '',
        'when':        extract_when_to_use(body),
        'source':      fm.get('source') or '',
        'risk':        fm.get('risk') or '',
        'tags':        fm.get('tags') if isinstance(fm.get('tags'), list) else [],
        'category':    (fm.get('category') or '').strip().lower() or None,
        'origin':      'real',
    }


def read_catalog_fallback(skill_dir, catalog_index):
    """Use catalog.json for a skill whose SKILL.md is a broken symlink."""
    name = skill_dir.name
    cat_entry = catalog_index.get(name)
    symlink_target = os.readlink(skill_dir / 'SKILL.md')
    # Derive source repo from symlink target path
    parts = Path(symlink_target).parts
    source_repo = parts[-3] if len(parts) >= 3 else 'external'

    return {
        'name':        name,
        'dir':         name,
        'description': cat_entry.get('description', '') if cat_entry else '',
        'when':        None,   # catalog.json doesn't store When to Use
        'source':      cat_entry.get('source', source_repo) if cat_entry else source_repo,
        'risk':        cat_entry.get('risk', '') if cat_entry else '',
        'tags':        cat_entry.get('tags', []) if cat_entry else [],
        'category':    (cat_entry.get('category') or '').strip().lower() if cat_entry else 'external',
        'origin':      'catalog' if cat_entry else 'stub',
        'source_repo': source_repo,
    }


def iter_skill_dirs(root):
    """Recursively yield every directory under root, depth-first, skipping META_DIRS subtrees.
    Mirrors build-catalog.js: symlinked directories are not followed (they may point
    outside the repo, e.g. to a plugin marketplace cache)."""
    for child in sorted(root.iterdir()):
        if child.is_symlink() or not child.is_dir() or child.name.startswith('.'):
            continue
        if child.name in META_DIRS:
            continue
        yield child
        yield from iter_skill_dirs(child)


def collect_skills():
    catalog_index = load_catalog_index()
    skills_by_category = defaultdict(list)

    for skill_dir in iter_skill_dirs(SKILLS_DIR):
        skill_md = skill_dir / 'SKILL.md'

        if skill_md.exists():
            # Real SKILL.md, or a symlink that resolves to one (readable either way)
            entry = read_real_skill(skill_dir)
        elif skill_md.is_symlink():
            # Broken symlink → fall back to catalog or stub
            entry = read_catalog_fallback(skill_dir, catalog_index)
        else:
            # No SKILL.md, not a symlink — just an organizational folder
            continue

        cat = entry['category'] or 'uncategorized'
        skills_by_category[cat].append(entry)

    return skills_by_category


# ── rendering ─────────────────────────────────────────────────────────────────

def render_skill(entry):
    lines = [f"### `{entry['dir']}`"]

    if entry['description']:
        lines.append(f"\n{entry['description']}")
    elif entry['origin'] == 'stub':
        lines.append(f"\n_Descripción no disponible — skill de repositorio externo (`{entry.get('source_repo', 'desconocido')}`)._")

    if entry['when']:
        lines.append(f"\n**Cuándo usar:**\n\n{entry['when']}")

    meta = []
    if entry['source']:
        meta.append(f"source: `{entry['source']}`")
    if entry['risk']:
        meta.append(f"risk: `{entry['risk']}`")
    tags = entry.get('tags', [])
    if tags:
        meta.append(f"tags: {', '.join(f'`{t}`' for t in tags[:5])}")
    if entry['origin'] in ('catalog', 'stub'):
        meta.append(f"_datos: {'catálogo' if entry['origin'] == 'catalog' else 'stub — sin datos'}_")
    if meta:
        lines.append(f"\n_{' · '.join(meta)}_")

    lines.append('\n---')
    return '\n'.join(lines)


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    print("Recolectando skills...")
    skills_by_category = collect_skills()

    total = sum(len(v) for v in skills_by_category.values())
    real    = sum(1 for v in skills_by_category.values() for e in v if e['origin'] == 'real')
    catalog = sum(1 for v in skills_by_category.values() for e in v if e['origin'] == 'catalog')
    stub    = sum(1 for v in skills_by_category.values() for e in v if e['origin'] == 'stub')
    print(f"  Total: {total} | SKILL.md real: {real} | catálogo: {catalog} | stub: {stub}")
    print(f"  Categorías: {len(skills_by_category)}")

    lines = [
        "# Skills Guide",
        f"\n> **{total} skills** documentadas · Actualizado: {date.today().isoformat()}\n",
        "> Fuentes por entrada: `SKILL.md` propio · `catalog.json` (repos externos) · stub (sin datos disponibles).\n",
        "## Índice de categorías\n",
    ]

    for cat in sorted(skills_by_category):
        count = len(skills_by_category[cat])
        anchor = re.sub(r'[^a-z0-9-]', '-', cat.lower())
        lines.append(f"- [{cat.title()} ({count})](#{anchor})")
    lines.append('')

    for cat in sorted(skills_by_category):
        entries = skills_by_category[cat]
        lines.append(f"---\n\n## {cat.title()}\n\n_{len(entries)} skills_\n")
        for entry in sorted(entries, key=lambda e: e['dir']):
            lines.append(render_skill(entry))
        lines.append('')

    OUTPUT.write_text('\n'.join(lines), encoding='utf-8')
    size_kb = OUTPUT.stat().st_size // 1024
    print(f"  Escrito: {OUTPUT} ({size_kb} KB)")


if __name__ == '__main__':
    main()
