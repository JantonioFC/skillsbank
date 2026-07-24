import { describe, it, expect, vi, beforeEach, Mock } from 'vitest';
import { act, fireEvent, screen, waitFor } from '@testing-library/react';
import { Home } from '../Home';
import { renderWithRouter } from '../../utils/testUtils';
import { createMockSkill } from '../../factories/skill';
import { useSkills } from '../../context/SkillContext';

// Mock useSkills hook
vi.mock('../../context/SkillContext', async (importOriginal) => {
  const actual = await importOriginal<any>();
  return { ...actual, useSkills: vi.fn() };
});

const virtuosoGridMock = vi.fn(({ totalCount, itemContent }: any) => (
  <div data-testid="virtuoso-grid">
    {Array.from({ length: totalCount || 0 }).map((_, index) => (
      <div key={index} data-testid="skill-item">
        {itemContent(index)}
      </div>
    ))}
  </div>
));

// Mock VirtuosoGrid to render items normally for easier testing
vi.mock('react-virtuoso', () => ({
  VirtuosoGrid: (props: any) => virtuosoGridMock(props),
}));

describe('Home', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  describe('Rendering', () => {
    it('should show loading spinner when loading is true', () => {
      (useSkills as Mock).mockReturnValue({
        skills: [],
        stars: {},
        loading: true,
        error: null,
      });

      renderWithRouter(<Home />, { useProvider: false });
      expect(screen.getByTestId('loader')).toBeInTheDocument();
    });

    it('should render skill cards when skills are loaded', async () => {
      const mockSkills = [
        createMockSkill({ id: 'skill-1', name: 'Skill 1' }),
        createMockSkill({ id: 'skill-2', name: 'Skill 2' }),
      ];

      (useSkills as Mock).mockReturnValue({
        skills: mockSkills,
        stars: {},
        loading: false,
        error: null,
      });

      renderWithRouter(<Home />, { useProvider: false });

      await waitFor(() => {
        expect(screen.getByText('@Skill 1')).toBeInTheDocument();
        expect(screen.getByText('@Skill 2')).toBeInTheDocument();
      });

      expect(virtuosoGridMock).toHaveBeenCalledWith(
        expect.objectContaining({ useWindowScroll: true }),
      );
    });

    it('should set homepage SEO metadata', async () => {
      const mockSkills = [
        createMockSkill({ id: 'skill-1', name: 'Skill 1' }),
      ];

      (useSkills as Mock).mockReturnValue({
        skills: mockSkills,
        stars: {},
        loading: false,
        error: null,
      });

      renderWithRouter(<Home />, { useProvider: false });

      await waitFor(() => {
        expect(document.title).toContain('Antigravity Awesome Skills');
      });

      expect(screen.getByRole('button', { name: /Copiar comando de instalación/i })).toBeInTheDocument();
      expect(screen.getAllByText(/npx antigravity-awesome-skills/i).length).toBeGreaterThan(0);
      expect(screen.getByText(/What is the difference between skills and MCP tools/i)).toBeInTheDocument();
      expect(document.querySelector('meta[property="og:title"]')).toHaveAttribute(
        'content',
        expect.stringContaining('Antigravity Awesome Skills'),
      );
    });

    it('should copy install command from hero CTA', async () => {
      (useSkills as Mock).mockReturnValue({
        skills: [],
        stars: {},
        loading: false,
        error: null,
      });

      renderWithRouter(<Home />, { useProvider: false });

      await waitFor(() => {
        expect(screen.getByRole('button', { name: /Copiar comando de instalación/i })).toBeInTheDocument();
      });

      vi.useFakeTimers();
      try {
        await act(async () => {
          fireEvent.click(screen.getByRole('button', { name: /Copiar comando de instalación/i }));
          await vi.runAllTimersAsync();
        });
      } finally {
        vi.useRealTimers();
      }

      expect(navigator.clipboard.writeText).toHaveBeenCalledWith('npx antigravity-awesome-skills');
    });
  });

  describe('Search and Filtering', () => {
    it('should filter skills based on search term', async () => {
      const mockSkills = [
        createMockSkill({ id: 'react', name: 'React Patterns' }),
        createMockSkill({ id: 'vue', name: 'Vue Basics' }),
      ];

      (useSkills as Mock).mockReturnValue({
        skills: mockSkills,
        stars: {},
        loading: false,
        error: null,
      });

      renderWithRouter(<Home />, { useProvider: false });

      const searchInput = screen.getByLabelText(/Buscar skills/i);
      fireEvent.change(searchInput, { target: { value: 'React' } });

      await waitFor(() => {
        expect(searchInput).toHaveValue('React');
        expect(screen.getByText('@React Patterns')).toBeInTheDocument();
        expect(screen.queryByText('@Vue Basics')).not.toBeInTheDocument();
      });
    });

    it('should filter skills by category', async () => {
      const mockSkills = [
        createMockSkill({ id: 's1', category: 'frontend', name: 'Frontend Skill' }),
        createMockSkill({ id: 's2', category: 'backend', name: 'Backend Skill' }),
      ];

      (useSkills as Mock).mockReturnValue({
        skills: mockSkills,
        stars: {},
        loading: false,
        error: null,
      });

      renderWithRouter(<Home />, { useProvider: false });

      const categorySelect = screen.getByLabelText(/Filtrar por categoría/i);
      fireEvent.change(categorySelect, { target: { value: 'frontend' } });

      await waitFor(() => {
        expect(categorySelect).toHaveValue('frontend');
        expect(screen.getByText('@Frontend Skill')).toBeInTheDocument();
        expect(screen.queryByText('@Backend Skill')).not.toBeInTheDocument();
      });
    });

    it('should disable the subcategory filter until a category is selected, then filter by it', async () => {
      const mockSkills = [
        createMockSkill({ id: 's1', category: 'frontend', subcategory: 'React', name: 'React Skill' }),
        createMockSkill({ id: 's2', category: 'frontend', subcategory: 'Vue', name: 'Vue Skill' }),
        createMockSkill({ id: 's3', category: 'backend', subcategory: 'React', name: 'Backend Skill' }),
      ];

      (useSkills as Mock).mockReturnValue({
        skills: mockSkills,
        stars: {},
        loading: false,
        error: null,
      });

      renderWithRouter(<Home />, { useProvider: false });

      const subcategorySelect = screen.getByLabelText(/Filtrar por subcategoría/i);
      expect(subcategorySelect).toBeDisabled();

      const categorySelect = screen.getByLabelText(/Filtrar por categoría/i);
      fireEvent.change(categorySelect, { target: { value: 'frontend' } });

      await waitFor(() => {
        expect(subcategorySelect).not.toBeDisabled();
      });

      fireEvent.change(subcategorySelect, { target: { value: 'React' } });

      await waitFor(() => {
        expect(subcategorySelect).toHaveValue('React');
        expect(screen.getByText('@React Skill')).toBeInTheDocument();
        expect(screen.queryByText('@Vue Skill')).not.toBeInTheDocument();
        expect(screen.queryByText('@Backend Skill')).not.toBeInTheDocument();
      });
    });
  });

  describe('User Settings and Sync', () => {
    it('hides sync actions on the public catalog and explains why', async () => {
      const mockSkills = [createMockSkill({ id: 'skill-1' })];

      (useSkills as Mock).mockReturnValue({
        skills: mockSkills,
        stars: { 'skill-1': 5 },
        loading: false,
        error: null,
        refreshSkills: vi.fn().mockResolvedValue(undefined),
      });

      renderWithRouter(<Home />, { useProvider: false });

      await waitFor(() => {
        expect(screen.queryByRole('button', { name: /Sincronizar/i })).not.toBeInTheDocument();
        expect(screen.getByText(/Modo catálogo público/i)).toBeInTheDocument();
        expect(screen.getByText(/flujo de trabajo exclusivo del equipo mantenedor/i)).toBeInTheDocument();
      });
    });
  });

  it('shows a catalog load error instead of a generic empty state', async () => {
    const refreshSkills = vi.fn().mockResolvedValue(undefined);

    (useSkills as Mock).mockReturnValue({
      skills: [],
      stars: {},
      loading: false,
      error: 'Non-JSON response from /skills.json (text/html)',
      refreshSkills,
    });

    renderWithRouter(<Home />, { useProvider: false });

    await waitFor(() => {
      expect(screen.getByText(/No se pudieron cargar las skills/i)).toBeInTheDocument();
      expect(screen.getByText(/Non-JSON response/i)).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: /Reintentar/i }));

    expect(refreshSkills).toHaveBeenCalled();
  });
});
