import { useState, useEffect, useMemo } from 'react';
import { Search, Filter, AlertCircle, RefreshCw, ArrowUpDown, Tag, X } from 'lucide-react';
import { VirtuosoGrid } from 'react-virtuoso';
import { useSkills } from '../context/SkillContext';
import { SkillCard } from '../components/SkillCard';
import type { SyncMessage, CategoryStats } from '../types';
import { usePageMeta } from '../hooks/usePageMeta';
import { buildHomeMeta, getHomeFaqItems } from '../utils/seo';
import { Link } from 'react-router-dom';

const conceptCards = [
  {
    title: 'Specialized plugins',
    body: 'Focused installable distributions for domains like web apps, security, documents, data, DevOps, QA, OSS, mobile, automation, and agent/MCP work.',
  },
  {
    title: 'Skills',
    body: 'Reusable SKILL.md playbooks that teach an AI assistant how to execute a workflow with better structure and context.',
  },
  {
    title: 'MCP tools',
    body: 'External capabilities and system integrations the assistant can call. Tools provide actions; skills tell the assistant how to use them well.',
  },
  {
    title: 'Bundles',
    body: 'Curated starting sets of recommended skills for a role, domain, or team that wants a smaller shortlist first.',
  },
  {
    title: 'Workflows',
    body: 'Ordered execution playbooks that show how to combine multiple skills step by step for a concrete outcome.',
  },
] as const;

const integrationGuides = [
  {
    name: 'Claude Code',
    href: 'https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/claude-code-skills.md',
    body: 'Install paths, starter prompts, plugin marketplace flow, and first skills to try.',
  },
  {
    name: 'Cursor',
    href: 'https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/cursor-skills.md',
    body: 'A practical guide for chat-first UI, frontend, and full-stack workflows in Cursor.',
  },
  {
    name: 'Codex CLI',
    href: 'https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/codex-cli-skills.md',
    body: 'How to use Antigravity Awesome Skills with Codex CLI for planning, implementation, testing, and review.',
  },
  {
    name: 'Gemini CLI',
    href: 'https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/gemini-cli-skills.md',
    body: 'A broad starting point for engineering, agent systems, integrations, and applied AI workflows.',
  },
] as const;

// `Sync Skills` is a maintainer/development affordance and must stay hidden
// on the public catalog unless VITE_ENABLE_SKILLS_SYNC=true (see README.md).
const syncFeatureEnabled = (
  (import.meta as ImportMeta & { env: Record<string, string | undefined> }).env.VITE_ENABLE_SKILLS_SYNC
  === 'true'
);

// 10-bucket taxonomy (confirmed 2026-07-23). skill.category now already
// stores these exact display strings (see tools/scripts/generate_index.py,
// TAXONOMY_MAP), so this is effectively an identity map — kept explicit so
// the display taxonomy is documented in one place and any stray legacy
// value still falls back gracefully via the default case below.
const CATEGORY_ES: Record<string, string> = {
  'AI & Agents': 'AI & Agents',
  'Desarrollo de Software': 'Desarrollo de Software',
  'Cloud, DevOps & Automatización': 'Cloud, DevOps & Automatización',
  'Seguridad': 'Seguridad',
  'Testing & Calidad': 'Testing & Calidad',
  'Diseño & Contenido': 'Diseño & Contenido',
  'Negocio & Marketing': 'Negocio & Marketing',
  'Gestión de Proyectos & Equipos': 'Gestión de Proyectos & Equipos',
  'Verticales Especializados': 'Verticales Especializados',
  'Meta & Productividad Personal': 'Meta & Productividad Personal',
  'uncategorized': 'Sin categoría',
};

export function translateCategory(cat: string): string {
  return CATEGORY_ES[cat] ?? cat.charAt(0).toUpperCase() + cat.slice(1).replace(/-/g, ' ');
}

// Palabras comunes a ignorar al extraer temas
const STOP_WORDS = new Set([
  'a', 'and', 'an', 'the', 'of', 'for', 'in', 'on', 'to', 'with',
  'by', 'at', 'as', 'or', 'is', 'be', 'my', 'up', 'do', 'it',
  'v2', 'v3', 'pro', 'new', 'old', 'ts', 'js', 'ms', 'py',
]);

function extractTopics(skillNames: string[]): string[] {
  const counts: Record<string, number> = {};
  skillNames.forEach(name => {
    name.split('-').forEach(token => {
      const t = token.toLowerCase().trim();
      if (t.length >= 3 && !STOP_WORDS.has(t) && !/^\d+$/.test(t)) {
        counts[t] = (counts[t] || 0) + 1;
      }
    });
  });
  return Object.entries(counts)
    .filter(([, count]) => count >= 3)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 40)
    .map(([topic]) => topic);
}

export function Home(): React.ReactElement {
  const { skills, stars, loading, error, refreshSkills } = useSkills();
  const [search, setSearch] = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [subcategoryFilter, setSubcategoryFilter] = useState('all');
  const [activeTopics, setActiveTopics] = useState<Set<string>>(new Set());
  const [sortBy, setSortBy] = useState('default');
  const [syncing, setSyncing] = useState(false);
  const [syncMsg, setSyncMsg] = useState<SyncMessage | null>(null);
  const [commandCopied, setCommandCopied] = useState(false);
  const installCommand = 'npx antigravity-awesome-skills';
  const repositoryLink = 'https://github.com/sickn33/antigravity-awesome-skills';
  const docsLink = 'https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/usage.md';
  const installLink = 'https://www.npmjs.com/package/antigravity-awesome-skills';
  const faqItems = getHomeFaqItems();
  const catalogCountLabel = skills.length > 0 ? skills.length.toLocaleString('en-US') : 'installable';

  usePageMeta(buildHomeMeta(skills.length));

  const copyInstallCommand = async () => {
    await navigator.clipboard.writeText(installCommand);
    setCommandCopied(true);
    window.setTimeout(() => setCommandCopied(false), 2000);
  };

  useEffect(() => {
    const timeoutId = window.setTimeout(() => {
      setDebouncedSearch(search);
    }, 300);

    return () => {
      window.clearTimeout(timeoutId);
    };
  }, [search]);

  const filteredSkills = useMemo(() => {
    let result = [...skills];

    if (debouncedSearch) {
      const lowerSearch = debouncedSearch.toLowerCase();
      result = result.filter(skill =>
        skill.name.toLowerCase().includes(lowerSearch) ||
        skill.description.toLowerCase().includes(lowerSearch)
      );
    }

    if (categoryFilter !== 'all') {
      result = result.filter(skill => skill.category === categoryFilter);
    }

    if (subcategoryFilter !== 'all') {
      result = result.filter(skill => skill.subcategory === subcategoryFilter);
    }

    if (activeTopics.size > 0) {
      result = result.filter(skill =>
        [...activeTopics].every(topic =>
          skill.name.toLowerCase().includes(topic) ||
          skill.description.toLowerCase().includes(topic)
        )
      );
    }

    if (sortBy === 'stars') {
      result = [...result].sort((a, b) => (stars[b.id] || 0) - (stars[a.id] || 0));
    } else if (sortBy === 'newest') {
      result = [...result].sort((a, b) => (b.date_added || '').localeCompare(a.date_added || ''));
    } else if (sortBy === 'az') {
      result = [...result].sort((a, b) => a.name.localeCompare(b.name));
    }

    return result;
  }, [debouncedSearch, categoryFilter, subcategoryFilter, activeTopics, sortBy, skills, stars]);

  const { categories, categoryStats } = useMemo(() => {
    const stats: CategoryStats = {};
    skills.forEach(skill => {
      stats[skill.category] = (stats[skill.category] || 0) + 1;
    });
    const cats = ['all', ...Object.keys(stats)
      .filter(cat => cat !== 'uncategorized')
      .sort((a, b) => stats[b] - stats[a]),
      ...(stats['uncategorized'] ? ['uncategorized'] : [])
    ];
    return { categories: cats, categoryStats: stats };
  }, [skills]);

  const { subcategories, subcategoryStats } = useMemo(() => {
    if (categoryFilter === 'all') {
      return { subcategories: [] as string[], subcategoryStats: {} as CategoryStats };
    }
    const stats: CategoryStats = {};
    skills
      .filter(skill => skill.category === categoryFilter && skill.subcategory)
      .forEach(skill => {
        const sub = skill.subcategory as string;
        stats[sub] = (stats[sub] || 0) + 1;
      });
    const subs = ['all', ...Object.keys(stats).sort((a, b) => stats[b] - stats[a])];
    return { subcategories: subs, subcategoryStats: stats };
  }, [skills, categoryFilter]);

  useEffect(() => {
    setSubcategoryFilter('all');
  }, [categoryFilter]);

  const topics = useMemo(() => extractTopics(skills.map(s => s.name)), [skills]);

  const toggleTopic = (topic: string) => {
    setActiveTopics(prev => {
      const next = new Set(prev);
      if (next.has(topic)) {
        next.delete(topic);
      } else {
        next.add(topic);
      }
      return next;
    });
  };

  const clearFilters = () => {
    setSearch('');
    setDebouncedSearch('');
    setCategoryFilter('all');
    setSubcategoryFilter('all');
    setActiveTopics(new Set());
    setSortBy('default');
  };

  const hasActiveFilters = search || categoryFilter !== 'all' || subcategoryFilter !== 'all' || activeTopics.size > 0;

  const handleSync = async () => {
    setSyncing(true);
    setSyncMsg(null);
    try {
      const res = await fetch('/api/refresh-skills', { method: 'POST' });
      const data = await res.json();
      if (data.success) {
        if (data.upToDate) {
          setSyncMsg({ type: 'info', text: 'ℹ️ Las skills ya están actualizadas.' });
        } else {
          setSyncMsg({ type: 'success', text: `✅ Sincronizadas ${data.count} skills.` });
          await refreshSkills();
        }
      } else {
        setSyncMsg({ type: 'error', text: String(data.error) });
      }
    } catch {
      setSyncMsg({ type: 'error', text: '❌ Error de red' });
    } finally {
      setSyncing(false);
      setTimeout(() => setSyncMsg(null), 5000);
    }
  };

  return (
    <div className="flex flex-col min-h-[calc(100vh-8rem)]">
      <div className="space-y-6 mb-8">

        {/* Hero */}
        <section className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 sm:p-7 shadow-sm">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400 mb-3">
            Empezá ahora
          </p>
          <h2 className="text-2xl sm:text-3xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
            Descubrí, instalá y usá skills de IA en minutos
          </h2>
          <p className="mt-3 text-sm sm:text-base leading-relaxed text-slate-600 dark:text-slate-300 max-w-4xl">
            Antigravity Awesome Skills es un catálogo de capacidades instalables para asistentes de IA.
            Instalá una vez y probá la skill directamente desde tu terminal sin saltar entre documentaciones.
            Buscá, filtrá y copiá el prompt listo para usar en un solo paso.
          </p>

          <div className="mt-6 flex flex-col gap-3 sm:flex-row sm:flex-wrap sm:items-stretch">
            <a
              href={repositoryLink}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center justify-center rounded-lg border border-slate-400/80 bg-white/80 px-4 py-2.5 text-sm font-semibold text-slate-900 shadow-[inset_0_1px_0_rgba(255,255,255,0.9),0_10px_20px_-16px_rgba(15,23,42,0.7)] transition-colors hover:border-slate-500 hover:bg-slate-100 dark:border-slate-600 dark:bg-slate-800/70 dark:text-slate-100 dark:hover:bg-slate-700"
            >
              Open the GitHub repository
            </a>
            <button
              onClick={copyInstallCommand}
              className="inline-flex items-center justify-center rounded-lg bg-slate-900 px-4 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-slate-800 dark:bg-slate-100 dark:text-slate-900 dark:hover:bg-white"
            >
              {commandCopied ? 'Comando copiado' : 'Copiar comando de instalación'}
            </button>
            <a
              href={installLink}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center justify-center rounded-lg border border-slate-400/80 bg-white/80 px-4 py-2.5 text-sm font-semibold text-slate-900 shadow-[inset_0_1px_0_rgba(255,255,255,0.9),0_10px_20px_-16px_rgba(15,23,42,0.7)] transition-colors hover:border-slate-500 hover:bg-slate-100 dark:border-slate-600 dark:bg-slate-800/70 dark:text-slate-100 dark:hover:bg-slate-700"
            >
              Instalar con npm
            </a>
            <a
              href={docsLink}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center justify-center rounded-lg border border-slate-400/80 bg-white/80 px-4 py-2.5 text-sm font-semibold text-slate-900 shadow-[inset_0_1px_0_rgba(255,255,255,0.9),0_10px_20px_-16px_rgba(15,23,42,0.7)] transition-colors hover:border-slate-500 hover:bg-slate-100 dark:border-slate-600 dark:bg-slate-800/70 dark:text-slate-100 dark:hover:bg-slate-700"
            >
              Leer documentación
            </a>
            <Link
              to="/plugins"
              className="inline-flex items-center justify-center rounded-lg border border-slate-400/80 bg-white/80 px-4 py-2.5 text-sm font-semibold text-slate-900 shadow-[inset_0_1px_0_rgba(255,255,255,0.9),0_10px_20px_-16px_rgba(15,23,42,0.7)] transition-colors hover:border-slate-500 hover:bg-slate-100 dark:border-slate-600 dark:bg-slate-800/70 dark:text-slate-100 dark:hover:bg-slate-700"
            >
              Compare specialized plugins
            </Link>
          </div>

          <div className="mt-5 flex flex-wrap items-center gap-2 text-xs text-slate-500 dark:text-slate-400">
            <span className="font-medium">Recommended command</span>
            <code className="rounded-md border border-slate-200 bg-slate-100 px-2 py-1 font-mono text-[11px] text-slate-700 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200">
              {installCommand}
            </code>
          </div>
          <p className="mt-3 text-xs text-slate-500 dark:text-slate-400">
            Comando recomendado:
            <span className="ml-2 rounded-md bg-slate-100 dark:bg-slate-800 px-2 py-1 font-mono">{installCommand}</span>
          </p>
        </section>

        {/* Encabezado + sincronizar */}
        <div className="flex flex-col space-y-4 md:flex-row md:items-center md:justify-between md:space-y-0">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-slate-100 mb-2">Explorar Skills</h1>
            <p className="text-slate-500 dark:text-slate-400">
              Descubrí {catalogCountLabel} capacidades agénticas para tu asistente de IA.
            </p>
          </div>
          <div className="flex items-center gap-3">
            {syncMsg && (
              <span className={`text-sm font-medium px-3 py-1.5 rounded-full ${syncMsg.type === 'success'
                ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
                : syncMsg.type === 'info'
                  ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400'
                  : 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
                }`}>
                {syncMsg.text}
              </span>
            )}
            {syncFeatureEnabled ? (
              <button
                onClick={handleSync}
                disabled={syncing}
                className="flex items-center space-x-2 px-4 py-2.5 rounded-lg font-medium text-sm bg-indigo-600 hover:bg-indigo-700 text-white disabled:opacity-50 disabled:cursor-wait transition-colors shadow-sm"
              >
                <RefreshCw className={`h-4 w-4 ${syncing ? 'animate-spin' : ''}`} />
                <span>{syncing ? 'Sincronizando...' : 'Sincronizar'}</span>
              </button>
            ) : (
              <span className="rounded-full bg-slate-100 dark:bg-slate-800 px-3 py-1.5 text-sm font-medium text-slate-600 dark:text-slate-300">
                Modo catálogo público
              </span>
            )}
          </div>
        </div>
        {!syncFeatureEnabled && (
          <p className="text-sm text-slate-500 dark:text-slate-400 -mt-2">
            La sincronización del catálogo es un flujo de trabajo exclusivo del equipo mantenedor en builds locales, por eso el sitio público en Pages siempre muestra el último catálogo publicado.
          </p>
        )}

        {/* Barra de búsqueda y filtros */}
        <div className="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm sticky top-0 z-40 space-y-3">
          <div className="flex flex-col space-y-3 md:flex-row md:items-center md:space-x-4 md:space-y-0">
            {/* Búsqueda de texto */}
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />
              <input
                type="text"
                placeholder="Buscar skills (ej: 'react', 'seguridad', 'python')..."
                aria-label="Buscar skills"
                className="w-full rounded-md border border-slate-200 bg-slate-50 px-9 py-2 text-sm outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-50"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>

            <div className="flex items-center space-x-2 overflow-x-auto pb-1 md:pb-0 scrollbar-hide shrink-0">
              {/* Filtro por categoría */}
              <Filter className="h-4 w-4 text-slate-500 shrink-0" />
              <select
                aria-label="Filtrar por categoría"
                className="h-9 rounded-md border border-slate-200 bg-slate-50 px-3 text-sm outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-50 min-w-[160px]"
                value={categoryFilter}
                onChange={(e) => setCategoryFilter(e.target.value)}
              >
                {categories.map(cat => (
                  <option key={cat} value={cat}>
                    {cat === 'all'
                      ? 'Todas las categorías'
                      : `${translateCategory(cat)} (${categoryStats[cat] || 0})`
                    }
                  </option>
                ))}
              </select>

              {/* Filtro por subcategoría */}
              <select
                aria-label="Filtrar por subcategoría"
                className="h-9 rounded-md border border-slate-200 bg-slate-50 px-3 text-sm outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-50 min-w-[160px] disabled:cursor-not-allowed disabled:opacity-50"
                value={subcategoryFilter}
                onChange={(e) => setSubcategoryFilter(e.target.value)}
                disabled={categoryFilter === 'all'}
              >
                {categoryFilter === 'all' ? (
                  <option value="all">Elegí una categoría primero</option>
                ) : (
                  subcategories.map(sub => (
                    <option key={sub} value={sub}>
                      {sub === 'all'
                        ? 'Todas las subcategorías'
                        : `${sub} (${subcategoryStats[sub] || 0})`
                      }
                    </option>
                  ))
                )}
              </select>

              {/* Ordenar */}
              <ArrowUpDown className="h-4 w-4 text-slate-500 shrink-0 ml-2" />
              <select
                aria-label="Ordenar skills"
                className="h-9 rounded-md border border-slate-200 bg-slate-50 px-3 text-sm outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-50 min-w-[140px]"
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
              >
                <option value="default">Por defecto</option>
                <option value="stars">⭐ Más valoradas</option>
                <option value="newest">🆕 Más recientes</option>
                <option value="az">🔤 A → Z</option>
              </select>

              {/* Limpiar filtros */}
              {hasActiveFilters && (
                <button
                  onClick={clearFilters}
                  className="h-9 flex items-center gap-1.5 px-3 rounded-md border border-slate-300 dark:border-slate-700 text-sm text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors shrink-0"
                  title="Limpiar filtros"
                >
                  <X className="h-3.5 w-3.5" />
                  Limpiar
                </button>
              )}
            </div>
          </div>

          {/* Chips de temas */}
          {topics.length > 0 && (
            <div className="space-y-1.5">
              <div className="flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-slate-400 dark:text-slate-500">
                <Tag className="h-3.5 w-3.5" />
                Temas
              </div>
              <div className="flex flex-wrap gap-1.5">
                {topics.map(topic => {
                  const isActive = activeTopics.has(topic);
                  return (
                    <button
                      key={topic}
                      onClick={() => toggleTopic(topic)}
                      className={`px-2.5 py-1 rounded-full text-xs font-medium transition-all border ${
                        isActive
                          ? 'bg-indigo-600 text-white border-indigo-600 shadow-sm'
                          : 'bg-slate-100 text-slate-600 border-slate-200 hover:bg-indigo-50 hover:border-indigo-300 hover:text-indigo-700 dark:bg-slate-800 dark:text-slate-300 dark:border-slate-700 dark:hover:bg-indigo-950/40 dark:hover:text-indigo-300'
                      }`}
                    >
                      {topic}
                    </button>
                  );
                })}
              </div>
            </div>
          )}
        </div>

        {/* Contador de resultados */}
        {!loading && (
          <div className="flex items-center justify-between text-sm text-slate-500 dark:text-slate-400 px-1">
            <span>
              {filteredSkills.length === skills.length
                ? `${skills.length} skills en total`
                : `${filteredSkills.length} de ${skills.length} skills`}
            </span>
            {activeTopics.size > 0 && (
              <span className="flex items-center gap-1">
                <Tag className="h-3.5 w-3.5" />
                Temas activos: {[...activeTopics].join(', ')}
              </span>
            )}
          </div>
        )}
      </div>

      {/* Grid de skills */}
      <div className="flex-1 min-h-[60vh] sm:min-h-[68vh] lg:min-h-[72vh] -mx-4">
        {loading ? (
          <div data-testid="loader" className="grid gap-6 px-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {[...Array(8)].map((_, i) => (
              <div key={i} className="animate-pulse rounded-lg border border-slate-200 p-6 h-48 bg-slate-100 dark:border-slate-800 dark:bg-slate-900" />
            ))}
          </div>
        ) : error && skills.length === 0 ? (
          <div className="py-12 text-center px-4 sm:px-6 lg:px-8">
            <AlertCircle className="mx-auto h-12 w-12 text-red-400" />
            <h3 className="mt-4 text-lg font-semibold text-slate-900 dark:text-slate-100">No se pudieron cargar las skills</h3>
            <p className="mt-2 text-slate-500 dark:text-slate-400">{error}</p>
            <button
              onClick={() => void refreshSkills()}
              className="mt-5 inline-flex items-center justify-center rounded-lg bg-slate-900 px-4 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-slate-800 dark:bg-slate-100 dark:text-slate-900 dark:hover:bg-white"
            >
              Reintentar
            </button>
          </div>
        ) : filteredSkills.length === 0 ? (
          <div className="py-12 text-center px-4 sm:px-6 lg:px-8">
            <AlertCircle className="mx-auto h-12 w-12 text-slate-400" />
            <h3 className="mt-4 text-lg font-semibold text-slate-900 dark:text-slate-100">Sin resultados</h3>
            <p className="mt-2 text-slate-500 dark:text-slate-400">Probá ajustando la búsqueda o los filtros.</p>
            <button
              onClick={clearFilters}
              className="mt-4 inline-flex items-center justify-center rounded-lg border border-slate-200 dark:border-slate-700 px-4 py-2.5 text-sm font-medium text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800"
            >
              Limpiar filtros
            </button>
          </div>
        ) : (
          <VirtuosoGrid
            useWindowScroll
            totalCount={filteredSkills.length}
            listClassName="grid gap-6 px-4 pb-8 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-4"
            itemContent={(index) => {
              const skill = filteredSkills[index];
              return <SkillCard key={skill.id} skill={skill} starCount={stars[skill.id] || 0} />;
            }}
          />
        )}
      </div>

      <div className="mt-12 space-y-10">
        <section className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm sm:p-7 dark:border-slate-800 dark:bg-slate-900">
          <p className="mb-3 text-xs font-semibold uppercase tracking-[0.2em] text-slate-500 dark:text-slate-400">
            Concepts
          </p>
          <h2 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
            Understand the system before scaling your setup
          </h2>
          <p className="mt-3 max-w-4xl text-sm leading-relaxed text-slate-600 sm:text-base dark:text-slate-300">
            The catalog is easier to navigate when you separate reusable playbooks from external tool integrations.
            Skills explain execution quality, MCP tools expose systems, bundles reduce decision overhead, and workflows
            map the operating sequence.
          </p>
          <div className="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            {conceptCards.map((card) => (
              <article
                key={card.title}
                className="rounded-xl border border-slate-200 bg-gradient-to-br from-white to-slate-50 p-4 dark:border-slate-800 dark:from-slate-900 dark:to-slate-950"
              >
                <h3 className="text-base font-semibold text-slate-900 dark:text-slate-100">{card.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-300">{card.body}</p>
              </article>
            ))}
          </div>
          <div className="mt-5 flex flex-wrap gap-3">
            <a
              href="https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/skills-vs-mcp-tools.md"
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center justify-center rounded-lg border border-slate-300 px-4 py-2.5 text-sm font-semibold text-slate-800 transition-colors hover:bg-slate-100 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
            >
              Read skills vs MCP/tools
            </a>
            <a
              href="https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/bundles.md"
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center justify-center rounded-lg border border-slate-300 px-4 py-2.5 text-sm font-semibold text-slate-800 transition-colors hover:bg-slate-100 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
            >
              Browse bundles
            </a>
            <a
              href="https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/workflows.md"
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center justify-center rounded-lg border border-slate-300 px-4 py-2.5 text-sm font-semibold text-slate-800 transition-colors hover:bg-slate-100 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
            >
              Explore workflows
            </a>
          </div>
        </section>

        <section className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm sm:p-7 dark:border-slate-800 dark:bg-slate-900">
          <p className="mb-3 text-xs font-semibold uppercase tracking-[0.2em] text-slate-500 dark:text-slate-400">
            Integration Guides
          </p>
          <h2 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
            Start from the guide that matches your assistant runtime
          </h2>
          <div className="mt-6 grid gap-4 md:grid-cols-2">
            {integrationGuides.map((guide) => (
              <a
                key={guide.name}
                href={guide.href}
                target="_blank"
                rel="noreferrer"
                className="rounded-xl border border-slate-200 bg-gradient-to-br from-white to-slate-50 p-4 transition-colors hover:border-slate-400 dark:border-slate-800 dark:from-slate-900 dark:to-slate-950 dark:hover:border-slate-600"
              >
                <h3 className="text-base font-semibold text-slate-900 dark:text-slate-100">{guide.name}</h3>
                <p className="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-300">{guide.body}</p>
              </a>
            ))}
          </div>
        </section>

        <section className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm sm:p-7 dark:border-slate-800 dark:bg-slate-900">
          <p className="mb-3 text-xs font-semibold uppercase tracking-[0.2em] text-slate-500 dark:text-slate-400">
            Quick FAQ
          </p>
          <h2 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
            Answers to the first questions most users ask
          </h2>
          <div className="mt-6 grid gap-4 lg:grid-cols-2">
            {faqItems.map((item) => (
              <article
                key={item.question}
                className="rounded-xl border border-slate-200 bg-gradient-to-br from-white to-slate-50 p-4 dark:border-slate-800 dark:from-slate-900 dark:to-slate-950"
              >
                <h3 className="text-base font-semibold text-slate-900 dark:text-slate-100">{item.question}</h3>
                <p className="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-300">{item.answer}</p>
              </article>
            ))}
          </div>
          <a
            href="https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/faq.md"
            target="_blank"
            rel="noreferrer"
            className="mt-5 inline-flex items-center justify-center rounded-lg border border-slate-300 px-4 py-2.5 text-sm font-semibold text-slate-800 transition-colors hover:bg-slate-100 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
          >
            Read the full FAQ
          </a>
        </section>
      </div>
    </div>
  );
}

export default Home;
