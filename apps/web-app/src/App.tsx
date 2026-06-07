import { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Link, Route, Routes } from 'react-router-dom';
import { Icon } from './components/ui/Icon';

const Home = lazy(() => import('./pages/Home'));
const SkillDetail = lazy(() => import('./pages/SkillDetail'));
const Plugins = lazy(() => import('./pages/Plugins'));

function App(): React.ReactElement {
  const logoSrc = `${import.meta.env.BASE_URL}Antigravity-Skills-logo.png`;

  return (
    <Router basename={import.meta.env.BASE_URL.replace(/\/$/, '') || '/'}>
      <div className="app-shell min-h-screen bg-[var(--surface-canvas)] text-[var(--text-primary)]">
        <header className="sticky top-0 z-50 border-b border-[var(--stroke-subtle)] bg-[var(--surface-card)]">
          <div className="mx-auto flex h-16 w-full max-w-screen-2xl items-center justify-between px-4 lg:px-6">
            <Link to="/" className="group inline-flex items-center gap-3 rounded-[var(--radius-sm)] px-1 py-1">
              <img
                src={logoSrc}
                alt="Antigravity Skills logo"
                className="h-9 w-auto object-contain transition-transform duration-[var(--motion-fast)] ease-[var(--motion-ease)] group-hover:scale-[1.015]"
              />
              <span className="hidden text-sm font-semibold tracking-[0.01em] text-[var(--text-primary)] sm:inline-block">
                Antigravity Skills
              </span>
            </Link>
            <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
              <nav className="flex items-center space-x-6 text-sm font-medium">
                <a
                  href="https://github.com/sickn33/antigravity-awesome-skills"
                  target="_blank"
                  rel="noreferrer"
                  className="flex items-center text-slate-600 transition-colors hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-50"
                >
                  <Github className="h-5 w-5 mr-2" />
                  Repositorio GitHub
                </a>
              </nav>
            </div>
          </div>
        </header>
        <main className="container max-w-screen-2xl mx-auto px-4 py-6">
          <Suspense
            fallback={
              <div className="flex min-h-[40vh] items-center justify-center text-sm text-slate-500 dark:text-slate-400">
                Cargando...
              </div>
            }
          >
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/skill/:id" element={<SkillDetail />} />
            </Routes>
          </Suspense>
        </main>
      </div>
    </Router>
  );
}

export default App;
