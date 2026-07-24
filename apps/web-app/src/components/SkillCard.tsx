import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { SkillStarButton } from './SkillStarButton';
import { Icon } from './ui/Icon';
import { translateCategory } from '../pages/Home';
import type { Skill } from '../types';

interface SkillCardProps {
  skill: Skill;
  starCount: number;
}

export const SkillCard = React.memo(({ skill, starCount }: SkillCardProps) => {
    return (
        <motion.div
            layout
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.2 }}
            className="h-full"
        >
            <Link
                to={`/skill/${skill.id}`}
                className="group flex flex-col h-full rounded-lg border border-slate-200 bg-white p-6 shadow-sm transition-all hover:bg-slate-50 hover:shadow-md dark:border-slate-800 dark:bg-slate-900 dark:hover:border-indigo-500/50"
            >
                <div className="relative mb-5 flex items-start justify-between gap-3">
                    <div className="flex min-w-0 items-center gap-2.5">
                        <div className="rounded-lg border border-slate-200 bg-slate-100 p-2 text-slate-700 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300">
                            <Icon name="book" size={20} className="h-5 w-5" />
                        </div>
                        <div className="min-w-0 flex flex-col gap-1">
                            <span className="truncate rounded-full border border-slate-200 bg-slate-100 px-2.5 py-1 text-xs font-medium text-slate-700 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300">
                                {skill.category ? translateCategory(skill.category) : 'Sin categoría'}
                            </span>
                            {skill.subcategory && (
                                <span className="truncate px-0.5 text-[11px] text-slate-500 dark:text-slate-400">
                                    {skill.subcategory}
                                </span>
                            )}
                        </div>
                    </div>

                    <SkillStarButton
                        skillId={skill.id}
                        communityCount={starCount}
                        variant="default"
                    />
                </div>

                <h3 className="mb-3 truncate text-base font-semibold text-slate-900 dark:text-slate-100">
                    @{skill.name}
                </h3>

                <div className="flex items-center justify-between text-xs text-slate-400 dark:text-slate-500 mb-3 pb-3 border-b border-slate-100 dark:border-slate-800">
                    <span>Riesgo: <span className="font-semibold text-slate-600 dark:text-slate-300">{skill.risk || 'desconocido'}</span></span>
                    {skill.date_added && (
                        <span className="ml-2">📅 {skill.date_added}</span>
                    )}
                </div>

                <div className="flex items-center text-sm font-medium text-indigo-600 dark:text-indigo-400 pt-2 mt-auto group-hover:translate-x-1 transition-transform">
                    Ver skill <Icon name="arrowRight" size={16} className="ml-1 h-4 w-4" />
                </div>
            </Link>
        </motion.div>
    );
});

SkillCard.displayName = 'SkillCard';
