import { useState, useEffect, useMemo, lazy, Suspense } from 'react';
import { translateCategory } from './Home';
import { useParams, Link } from 'react-router-dom';
import { SkillStarButton } from '../components/SkillStarButton';
import { Icon } from '../components/ui/Icon';
import { useSkills } from '../context/SkillContext';
import { usePageMeta } from '../hooks/usePageMeta';
import { buildSkillFallbackMeta, buildSkillMeta, selectTopSkills } from '../utils/seo';
import { getSkillMarkdownCandidateUrls } from '../utils/publicAssetUrls';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';

// Lazy load heavy markdown component
const Markdown = lazy(() => import('react-markdown'));

function looksLikeHtmlDocument(text: string): boolean {
  const trimmed = text.trim().toLowerCase();
  return trimmed.startsWith('<!doctype html') || trimmed.startsWith('<html');
}

/** Split YAML frontmatter (--- ... ---) and markdown body */
function splitFrontmatter(md: string): { frontmatter: string; body: string } {
  const match = md.match(/^(---[\s\S]*?---)\s*\n?/);

  if (!match) {
    return { frontmatter: '', body: md };
  }

  return {
    frontmatter: match[1],
    body: md.slice(match[0].length),
  };
}

function parseFrontmatterRows(frontmatter: string): Array<{ key: string; value: string }> {
  return frontmatter
    .split('\n')
    .map(line => line.trim())
    .filter(line => line && line !== '---')
    .map(line => {
      const separatorIndex = line.indexOf(':');

      if (separatorIndex === -1) {
        return null;
      }

      const key = line.slice(0, separatorIndex).trim();
      const rawValue = line.slice(separatorIndex + 1).trim();
      const value = rawValue.replace(/^"(.*)"$/, '$1').replace(/^'(.*)'$/, '$1');

      return key ? { key, value } : null;
    })
    .filter((row): row is { key: string; value: string } => row !== null);
}

interface RouteParams {
  id: string;
  [key: string]: string | undefined;
}

export function SkillDetail(): React.ReactElement {
  const { id } = useParams<RouteParams>();
  const { skills, stars, loading: contextLoading } = useSkills();
  const [content, setContent] = useState('');
  const [contentLoading, setContentLoading] = useState(true);
  const [copied, setCopied] = useState(false);
  const [copiedFull, setCopiedFull] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [customContext, setCustomContext] = useState('');
  const [commandCopied, setCommandCopied] = useState(false);
  const [retryToken, setRetryToken] = useState(0);
  const installCommand = 'npx antigravity-awesome-skills';
  const skill = useMemo(() => skills.find(s => s.id === id), [skills, id]);

  const topPrioritySkills = useMemo(() => selectTopSkills(skills), [skills]);
  const topPrioritySkillSet = useMemo(() => new Set(topPrioritySkills.map(topSkill => topSkill.id)), [topPrioritySkills]);

  const canonicalPath = useMemo(() => {
    const safeId = id ? id : 'skill';
    return `/skill/${encodeURIComponent(safeId)}`;
  }, [id]);

  const isPriority = useMemo(() => {
    if (!skill) {
      return false;
    }

    return topPrioritySkillSet.has(skill.id);
  }, [skill, topPrioritySkillSet]);

  usePageMeta(
    useMemo(() => {
      if (!skill) {
        return buildSkillFallbackMeta(id || 'skill');
      }

      return buildSkillMeta(skill, isPriority, canonicalPath);
    }, [id, skill, isPriority, canonicalPath])
  );

  const communityCount = useMemo(() => (id ? stars[id] || 0 : 0), [stars, id]);
  const { frontmatter, body: markdownBody } = useMemo(() => splitFrontmatter(content), [content]);
  const frontmatterRows = useMemo(() => parseFrontmatterRows(frontmatter), [frontmatter]);

  useEffect(() => {
    if (contextLoading || !skill) return;

    const loadMarkdown = async () => {
      setContentLoading(true);
      setError(null);
      try {
        const cleanPath = skill.path.startsWith('skills/')
          ? skill.path.replace('skills/', '')
          : skill.path;

        const candidateUrls = getSkillMarkdownCandidateUrls({
          baseUrl: import.meta.env.BASE_URL,
          origin: window.location.origin,
          pathname: window.location.pathname,
          documentBaseUrl: window.document.baseURI,
          skillPath: `skills/${cleanPath}`,
        });

        let markdown: string | null = null;
        let lastError: Error | null = null;

        for (const url of candidateUrls) {
          try {
            const mdRes = await fetch(url);
            if (!mdRes.ok) {
              throw new Error(`Request failed (${mdRes.status}) for ${url}`);
            }

            const text = await mdRes.text();
            if (looksLikeHtmlDocument(text)) {
              throw new Error(`HTML fallback returned instead of markdown for ${url}`);
            }

            markdown = text;
            break;
          } catch (err) {
            lastError = err instanceof Error ? err : new Error(String(err));
          }
        }

        if (markdown === null) {
          throw lastError || new Error('Skill file not found');
        }

        setContent(markdown);
      } catch (err) {
        console.error('Failed to load skill content', err);
        setError(err instanceof Error ? err.message : 'Could not load skill content.');
      } finally {
        setContentLoading(false);
      }
    };

    loadMarkdown();
  }, [skill, contextLoading, retryToken]);

  const copyToClipboard = () => {
    if (!skill) return;

    const basePrompt = `Use @${skill.name}`;
    const finalPrompt = customContext.trim()
      ? `${basePrompt}\n\nContext:\n${customContext}`
      : basePrompt;

    navigator.clipboard.writeText(finalPrompt);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const copyInstallCommand = async () => {
    await navigator.clipboard.writeText(installCommand);
    setCommandCopied(true);
    window.setTimeout(() => setCommandCopied(false), 2000);
  };

  const copyFullToClipboard = () => {
    const finalPrompt = customContext.trim()
      ? `${content}\n\nContext:\n${customContext}`
      : content;

    navigator.clipboard.writeText(finalPrompt);
    setCopiedFull(true);
    setTimeout(() => setCopiedFull(false), 2000);
  };

  if (!contextLoading && !skill) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] text-center px-4">
        <h2 className="text-xl font-bold mb-2">Error al cargar la skill</h2>
        <p className="text-slate-600 dark:text-slate-400">Skill no encontrada en el registro.</p>
        <Link to="/" className="mt-4 text-indigo-600 hover:underline">Volver al catálogo</Link>
      </div>
    );
  }

  if (contextLoading || (contentLoading && !error)) {
    return (
      <div className="flex min-h-[55vh] items-center justify-center" data-testid="loader">
        <div className="rounded-full border border-slate-200 bg-white/90 p-4 shadow-sm backdrop-blur dark:border-slate-800 dark:bg-slate-950/80">
          <Icon name="loader" size={32} className="h-8 w-8 animate-spin text-teal-600" />
        </div>
      </div>
    );
  }

  // If we're here, contextLoading is false, skill is defined, and content loading is finished (or errored)
  if (error || !skill) {
    return (
      <div className="max-w-2xl mx-auto text-center py-12">
        <AlertTriangle className="h-12 w-12 text-red-500 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">Error al cargar el contenido</h2>
        <p className="text-slate-500 mt-2">{error || 'No se pudo cargar la skill.'}</p>
        <button
          onClick={() => setRetryToken((value) => value + 1)}
          className="mt-6 inline-flex items-center justify-center rounded-full bg-teal-600 px-5 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-teal-700"
        >
          Reintentar
        </button>
        <Link to="/" className="mt-8 inline-flex items-center text-indigo-600 font-medium hover:underline">
          <ArrowLeft className="mr-2 h-4 w-4" /> Volver al catálogo
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <Link to="/" className="inline-flex items-center text-sm font-medium text-slate-500 hover:text-indigo-600 transition-colors mb-4 group">
          <ArrowLeft className="mr-1 h-4 w-4 transform group-hover:-translate-x-1 transition-transform" />
          Volver al catálogo
        </Link>

        <div className="relative flex flex-col justify-between gap-5 rounded-2xl border border-slate-200/80 bg-white/95 p-6 shadow-sm backdrop-blur dark:border-slate-800 dark:bg-slate-900/80 md:flex-row md:items-center">
          <div className="flex-1">
            <div className="flex items-center space-x-3 mb-2 flex-wrap gap-2">
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-100 text-indigo-700 dark:bg-indigo-900/50 dark:text-indigo-400 uppercase tracking-wide">
                {translateCategory(skill.category)}
              </span>
              {skill.source && (
                <span className="rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-medium text-slate-600 dark:bg-slate-800 dark:text-slate-300">
                  {skill.source}
                </span>
              )}
              {skill.date_added && (
                <span className="rounded-full bg-green-100 px-2.5 py-0.5 text-xs font-medium text-green-700 dark:bg-green-900/50 dark:text-green-300">
                  Added {skill.date_added}
                </span>
              )}
            </div>
            <div className="flex items-center gap-3">
              <h1 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-4xl">
                @{skill.name}
              </h1>
              <SkillStarButton skillId={skill.id} communityCount={communityCount} variant="compact" />
            </div>
            <p className="mt-3 max-w-3xl text-base leading-relaxed text-slate-600 dark:text-slate-300 sm:text-lg">
              {skill.description}
            </p>
          </div>

          <div className="flex flex-col gap-2 sm:flex-row">
            <button
              onClick={copyToClipboard}
              className="flex min-w-[148px] items-center justify-center space-x-2 rounded-full border border-slate-300 bg-white px-4 py-2.5 font-medium text-slate-900 transition-colors hover:border-slate-400 hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:hover:border-slate-500 dark:hover:bg-slate-800"
            >
              {copied ? <Check className="h-4 w-4 text-green-600 dark:text-green-400" /> : <Copy className="h-4 w-4" />}
              <span>{copied ? '¡Copiado!' : 'Copiar @Skill'}</span>
            </button>
            <button
              onClick={copyFullToClipboard}
              className="flex min-w-[148px] items-center justify-center space-x-2 rounded-full bg-slate-900 px-4 py-2.5 font-medium text-white transition-colors hover:bg-slate-800 dark:bg-slate-50 dark:text-slate-900 dark:hover:bg-slate-200"
            >
              {copiedFull ? <Check className="h-4 w-4 text-green-400" /> : <FileCode className="h-4 w-4" />}
              <span>{copiedFull ? '¡Contenido copiado!' : 'Copiar contenido completo'}</span>
            </button>
          </div>
        </div>

        <div className="mt-6 bg-white dark:bg-slate-900 p-6 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
          <div className="rounded-lg border border-slate-200 bg-slate-50 dark:border-slate-700 dark:bg-slate-900 p-4 mb-4">
            <p className="text-xs uppercase tracking-wide text-slate-500 dark:text-slate-400 font-semibold">
              Usarla ahora
            </p>
            <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">
              Instalá el paquete, abrí tu workspace y ejecutá el prompt de esta skill directamente.
            </p>
            <div className="mt-3 flex flex-wrap items-center gap-3">
              <code className="inline-block rounded-md border border-slate-800 bg-slate-900 px-3 py-2 font-mono text-sm text-slate-50">
                {installCommand}
              </code>
              <button
                onClick={copyInstallCommand}
                className="inline-flex items-center text-sm font-medium text-teal-700 transition-colors hover:text-teal-600 dark:text-teal-300 dark:hover:text-teal-200"
              >
                {commandCopied ? 'Copiado' : 'Copiar comando'}
              </button>
            </div>
          </div>

          <label htmlFor="context" className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
            Constructor de prompt (opcional)
          </label>
          <p className="text-xs text-slate-500 dark:text-slate-400 mb-3">
            Agregá detalles específicos (ej: &quot;Usá React 19 y Tailwind&quot;). El botón &quot;Copiar @Skill&quot; adjuntará tu contexto automáticamente.
          </p>
          <textarea
            id="context"
            rows={3}
            className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-4 py-3 text-sm text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 outline-none transition-all resize-y"
            placeholder="Escribí los requerimientos específicos de tu tarea..."
            value={customContext}
            onChange={(e) => setCustomContext(e.target.value)}
          />
        </div>
      </div>

      <div className="overflow-hidden rounded-3xl border border-slate-200/80 bg-white shadow-sm dark:border-slate-800 dark:bg-slate-900">
        <div className="p-6 sm:p-8">
          {frontmatterRows.length > 0 && (
            <div className="mb-6">
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400 mb-2">
                Metadatos de la skill
              </p>
              <div className="overflow-x-auto rounded-xl border border-slate-200 dark:border-slate-700">
                <table className="min-w-full border-collapse text-left text-sm">
                  <thead>
                    <tr className="bg-slate-50 dark:bg-slate-950/80">
                      {frontmatterRows.map(({ key }) => (
                        <th
                          key={key}
                          className="border-b border-slate-200 px-4 py-2 font-semibold text-slate-800 dark:border-slate-700 dark:text-slate-100"
                        >
                          {key}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    <tr className="bg-white dark:bg-slate-900">
                      {frontmatterRows.map(({ key, value }) => (
                        <td
                          key={key}
                          className="align-top border-t border-slate-200 px-4 py-2 text-slate-700 dark:border-slate-700 dark:text-slate-200"
                        >
                          {value}
                        </td>
                      ))}
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          )}

          <div className="markdown-body" style={{ backgroundColor: 'transparent' }}>
            <Suspense fallback={<div className="h-24 animate-pulse rounded-lg bg-slate-100 dark:bg-slate-800"></div>}>
              <Markdown
                remarkPlugins={[remarkGfm]}
                rehypePlugins={[rehypeHighlight]}
              >
                {markdownBody}
              </Markdown>
            </Suspense>
          </div>
        </div>
      </div>
    </div>
  );
}

export default SkillDetail;
