
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Search, Filter, Book, AlertCircle, ArrowRight } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export function Home() {
    const [skills, setSkills] = useState([]);
    const [filteredSkills, setFilteredSkills] = useState([]);
    const [search, setSearch] = useState('');
    const [categoryFilter, setCategoryFilter] = useState('all');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('/skills.json')
            .then(res => res.json())
            .then(data => {
                setSkills(data);
                setFilteredSkills(data);
                setLoading(false);
            })
            .catch(err => {
                console.error("Failed to load skills", err);
                setLoading(false);
            });
    }, []);

    useEffect(() => {
        let result = skills;

        if (search) {
            const lowerSearch = search.toLowerCase();
            result = result.filter(skill =>
                skill.name.toLowerCase().includes(lowerSearch) ||
                skill.description.toLowerCase().includes(lowerSearch)
            );
        }

        if (categoryFilter !== 'all') {
            result = result.filter(skill => skill.category === categoryFilter);
        }

        setFilteredSkills(result);
    }, [search, categoryFilter, skills]);

    const categories = ['all', ...new Set(skills.map(s => s.category).filter(Boolean))];

    return (
        <div className="space-y-8">
            <div className="flex flex-col space-y-4 md:flex-row md:items-center md:justify-between md:space-y-0">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-slate-100 mb-2">Explore Skills</h1>
                    <p className="text-slate-500 dark:text-slate-400">Discover {skills.length} agentic capabilities for your AI assistant.</p>
                </div>
            </div>

            <div className="flex flex-col space-y-4 md:flex-row md:items-center md:space-x-4 md:space-y-0 bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm sticky top-20 z-40">
                <div className="relative flex-1">
                    <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />
                    <input
                        type="text"
                        placeholder="Search skills (e.g., 'react', 'security', 'python')..."
                        className="w-full rounded-md border border-slate-200 bg-slate-50 px-9 py-2 text-sm outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-50"
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                    />
                </div>
                <div className="flex items-center space-x-2 overflow-x-auto pb-2 md:pb-0 scrollbar-hide">
                    <Filter className="h-4 w-4 text-slate-500 shrink-0" />
                    <select
                        className="h-9 rounded-md border border-slate-200 bg-slate-50 px-3 text-sm outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-50 min-w-[150px]"
                        value={categoryFilter}
                        onChange={(e) => setCategoryFilter(e.target.value)}
                    >
                        {categories.map(cat => (
                            <option key={cat} value={cat}>{cat.charAt(0).toUpperCase() + cat.slice(1)}</option>
                        ))}
                    </select>
                </div>
            </div>

            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                <AnimatePresence>
                    {loading ? (
                        [...Array(8)].map((_, i) => (
                            <div key={i} className="animate-pulse rounded-lg border border-slate-200 p-6 h-48 bg-slate-100 dark:border-slate-800 dark:bg-slate-900">
                            </div>
                        ))
                    ) : filteredSkills.length === 0 ? (
                        <div className="col-span-full py-12 text-center">
                            <AlertCircle className="mx-auto h-12 w-12 text-slate-400" />
                            <h3 className="mt-4 text-lg font-semibold text-slate-900 dark:text-slate-100">No skills found</h3>
                            <p className="mt-2 text-slate-500 dark:text-slate-400">Try adjusting your search or filter.</p>
                        </div>
                    ) : (
                        filteredSkills.map((skill) => (
                            <motion.div
                                key={skill.id}
                                layout
                                initial={{ opacity: 0, scale: 0.95 }}
                                animate={{ opacity: 1, scale: 1 }}
                                exit={{ opacity: 0, scale: 0.95 }}
                                transition={{ duration: 0.2 }}
                            >
                                <Link
                                    to={`/skill/${skill.id}`}
                                    className="group flex flex-col h-full rounded-lg border border-slate-200 bg-white p-6 shadow-sm transition-all hover:bg-slate-50 hover:shadow-md dark:border-slate-800 dark:bg-slate-900 dark:hover:border-indigo-500/50"
                                >
                                    <div className="flex items-center justify-between mb-4">
                                        <div className="flex items-center space-x-2">
                                            <div className="p-2 bg-indigo-50 dark:bg-indigo-950/30 rounded-md">
                                                <Book className="h-5 w-5 text-indigo-600 dark:text-indigo-400" />
                                            </div>
                                            <span className="text-xs font-medium px-2 py-1 rounded-full bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400">
                                                {skill.category || 'Uncategorized'}
                                            </span>
                                        </div>
                                    </div>

                                    <h3 className="text-lg font-bold text-slate-900 dark:text-slate-50 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors mb-2 line-clamp-1">
                                        @{skill.name}
                                    </h3>

                                    <p className="text-sm text-slate-500 dark:text-slate-400 line-clamp-3 mb-4 flex-grow">
                                        {skill.description}
                                    </p>

                                    <div className="flex items-center text-sm font-medium text-indigo-600 dark:text-indigo-400 pt-4 mt-auto border-t border-slate-100 dark:border-slate-800 group-hover:translate-x-1 transition-transform">
                                        Read Skill <ArrowRight className="ml-1 h-4 w-4" />
                                    </div>
                                </Link>
                            </motion.div>
                        ))
                    )}
                </AnimatePresence>
            </div>
        </div>
    );
}
