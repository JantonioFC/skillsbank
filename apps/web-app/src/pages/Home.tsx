import { useState, useEffect, useMemo, useCallback } from 'react';
import { Search, Filter, AlertCircle, RefreshCw, ArrowUpDown, Tag, X } from 'lucide-react';
import { VirtuosoGrid } from 'react-virtuoso';
import debounce from 'lodash.debounce';
import { useSkills } from '../context/SkillContext';
import { SkillCard } from '../components/SkillCard';
import type { SyncMessage, CategoryStats } from '../types';
import { usePageMeta } from '../hooks/usePageMeta';
import { APP_HOME_CATALOG_COUNT, buildHomeMeta } from '../utils/seo';

const CATEGORY_ES: Record<string, string> = {
  'uncategorized': 'Sin categoría',
  'cloud': 'Nube',
  'ai-ml': 'IA / ML',
  'development': 'Desarrollo',
  'security': 'Seguridad',
  'business': 'Negocios',
  'web-development': 'Desarrollo web',
  'marketing': 'Marketing',
  'content': 'Contenido',
  'workflow': 'Flujo de trabajo',
  'automation': 'Automatización',
  'testing': 'Testing',
  'backend': 'Backend',
  'meta': 'Meta',
  'devops': 'DevOps',
  'engineering': 'Ingeniería',
  'architecture': 'Arquitectura',
  'c-level-advisor': 'C-Level',
  'mobile': 'Mobile',
  'engineering-team': 'Equipo de ingeniería',
  'project-management': 'Gestión de proyectos',
  'api-integration': 'Integración API',
  'database': 'Base de datos',
  'marketing-skill': 'Marketing',
  'game-development': 'Desarrollo de juegos',
  'code': 'Código',
  'health': 'Salud',
  'data': 'Datos',
  'design': 'Diseño',
  'ai-agents': 'Agentes IA',
  'front-end': 'Frontend',
  'code-quality': 'Calidad de código',
  'reliability': 'Confiabilidad',
  'product-team': 'Producto',
  'data-ai': 'Datos / IA',
  'framework': 'Framework',
  'productivity': 'Productividad',
  'data-science': 'Ciencia de datos',
  'science': 'Ciencia',
  'test-automation': 'Automatización de tests',
  'legal': 'Legal',
  'blockchain': 'Blockchain',
  'memory': 'Memoria',
  'graphics-processing': 'Gráficos',
  'frontend': 'Frontend',
  'create': 'Crear',
  'andruia': 'Andru.ia',
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
  const [activeTopics, setActiveTopics] = useState<Set<string>>(new Set());
  const [sortBy, setSortBy] = useState('default');
  const [syncing, setSyncing] = useState(false);
  const [syncMsg, setSyncMsg] = useState<SyncMessage | null>(null);
  const [commandCopied, setCommandCopied] = useState(false);
  const installCommand = 'npx antigravity-awesome-skills';
  const docsLink = 'https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/usage.md';
  const installLink = 'https://www.npmjs.com/package/antigravity-awesome-skills';

  usePageMeta(buildHomeMeta(skills.length));

  const copyInstallCommand = async () => {
    await navigator.clipboard.writeText(installCommand);
    setCommandCopied(true);
    window.setTimeout(() => setCommandCopied(false), 2000);
  };

  const debouncedSetSearch = useCallback(
    debounce((value: string) => setDebouncedSearch(value), 300),
    []
  );

  useEffect(() => {
    debouncedSetSearch(search);
  }, [search, debouncedSetSearch]);

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
  }, [debouncedSearch, categoryFilter, activeTopics, sortBy, skills, stars]);

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

  const topics = useMemo(() => extractTopics(skills.map(s => s.name)), [skills]);

  const toggleTopic = (topic: string) => {
    setActiveTopics(prev => {
      const next = new Set(prev);
      next.has(topic) ? next.delete(topic) : next.add(topic);
      return next;
    });
  };

  const clearFilters = () => {
    setSearch('');
    setDebouncedSearch('');
    setCategoryFilter('all');
    setActiveTopics(new Set());
    setSortBy('default');
  };

  const hasActiveFilters = search || categoryFilter !== 'all' || activeTopics.size > 0;

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
        setSyncMsg({ type: 'error', text: `❌ ${data.error}` });
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
          <div className="mt-5 flex flex-col gap-3 sm:flex-row sm:items-stretch">
            <button
              onClick={copyInstallCommand}
              className="inline-flex items-center justify-center rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-indigo-700"
            >
              {commandCopied ? 'Comando copiado' : 'Copiar comando de instalación'}
            </button>
            <a
              href={installLink}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center justify-center rounded-lg border border-indigo-600 text-sm font-semibold text-indigo-700 dark:text-indigo-200 px-4 py-2.5 hover:bg-indigo-50 dark:hover:bg-slate-800"
            >
              Instalar con npm
            </a>
            <a
              href={docsLink}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center justify-center rounded-lg border border-slate-200 dark:border-slate-700 text-sm font-semibold text-slate-700 dark:text-slate-200 px-4 py-2.5 hover:bg-slate-50 dark:hover:bg-slate-800"
            >
              Leer documentación
            </a>
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
              Descubrí {Math.max(skills.length, APP_HOME_CATALOG_COUNT)}+ capacidades agénticas para tu asistente de IA.
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
            <button
              onClick={handleSync}
              disabled={syncing}
              className="flex items-center space-x-2 px-4 py-2.5 rounded-lg font-medium text-sm bg-indigo-600 hover:bg-indigo-700 text-white disabled:opacity-50 disabled:cursor-wait transition-colors shadow-sm"
            >
              <RefreshCw className={`h-4 w-4 ${syncing ? 'animate-spin' : ''}`} />
              <span>{syncing ? 'Sincronizando...' : 'Sincronizar'}</span>
            </button>
          </div>
        </div>

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
          <div data-testid="loader" className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 px-4">
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
              className="mt-5 inline-flex items-center justify-center rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-indigo-700"
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
            listClassName="grid gap-6 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-4 pb-8 px-4"
            itemContent={(index) => {
              const skill = filteredSkills[index];
              return <SkillCard key={skill.id} skill={skill} starCount={stars[skill.id] || 0} />;
            }}
          />
        )}
      </div>
    </div>
  );
}

export default Home;
