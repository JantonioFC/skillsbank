---
name: senior-frontend
risk: unknown
source: community
description: Senior frontend
---
=======
description: Frontend development skill for React, Next.js, TypeScript, and Tailwind CSS applications. Use when building React components, optimizing Next.js performance, analyzing bundle sizes, scaffolding frontend projects, implementing accessibility, or reviewing frontend code quality.
risk: safe
source: https://github.com/alirezarezvani/claude-skills
date_added: "2026-03-07"
---

>>>>>>> origin/main
# Senior Frontend

Frontend development patterns, performance optimization, and automation tools for React/Next.js applications.

<<<<<<< HEAD
=======
## When to Use
- Use when scaffolding a new React or Next.js project with TypeScript and Tailwind CSS.
- Use when generating new components or custom hooks.
- Use when analyzing and optimizing bundle sizes for frontend applications.
- Use to implement or review advanced React patterns like Compound Components or Render Props.
- Use to ensure accessibility compliance and implement robust testing strategies.

>>>>>>> origin/main
## Table of Contents

- [Project Scaffolding](#project-scaffolding)
- [Component Generation](#component-generation)
- [Bundle Analysis](#bundle-analysis)
- [React Patterns](#react-patterns)
- [Next.js Optimization](#nextjs-optimization)
- [Accessibility and Testing](#accessibility-and-testing)

---

## Project Scaffolding

Generate a new Next.js or React project with TypeScript, Tailwind CSS, and best practice configurations.

### Workflow: Create New Frontend Project

1. Run the scaffolder with your project name and template:
<<<<<<< HEAD
=======

>>>>>>> origin/main
   ```bash
   python scripts/frontend_scaffolder.py my-app --template nextjs
   ```

2. Add optional features (auth, api, forms, testing, storybook):
<<<<<<< HEAD
=======

>>>>>>> origin/main
   ```bash
   python scripts/frontend_scaffolder.py dashboard --template nextjs --features auth,api
   ```

3. Navigate to the project and install dependencies:
<<<<<<< HEAD
=======

>>>>>>> origin/main
   ```bash
   cd my-app && npm install
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

### Scaffolder Options

<<<<<<< HEAD
| Option | Description |
|--------|-------------|
| `--template nextjs` | Next.js 14+ with App Router and Server Components |
| `--template react` | React + Vite with TypeScript |
| `--features auth` | Add NextAuth.js authentication |
| `--features api` | Add React Query + API client |
| `--features forms` | Add React Hook Form + Zod validation |
| `--features testing` | Add Vitest + Testing Library |
| `--dry-run` | Preview files without creating them |
=======
| Option               | Description                                       |
| -------------------- | ------------------------------------------------- |
| `--template nextjs`  | Next.js 14+ with App Router and Server Components |
| `--template react`   | React + Vite with TypeScript                      |
| `--features auth`    | Add NextAuth.js authentication                    |
| `--features api`     | Add React Query + API client                      |
| `--features forms`   | Add React Hook Form + Zod validation              |
| `--features testing` | Add Vitest + Testing Library                      |
| `--dry-run`          | Preview files without creating them               |
>>>>>>> origin/main

### Generated Structure (Next.js)

```
my-app/
├── app/
│   ├── layout.tsx        # Root layout with fonts
│   ├── page.tsx          # Home page
│   ├── globals.css       # Tailwind + CSS variables
│   └── api/health/route.ts
├── components/
│   ├── ui/               # Button, Input, Card
│   └── layout/           # Header, Footer, Sidebar
├── hooks/                # useDebounce, useLocalStorage
├── lib/                  # utils (cn), constants
├── types/                # TypeScript interfaces
├── tailwind.config.ts
├── next.config.js
└── package.json
```

---

## Component Generation

Generate React components with TypeScript, tests, and Storybook stories.

### Workflow: Create a New Component

1. Generate a client component:
<<<<<<< HEAD
=======

>>>>>>> origin/main
   ```bash
   python scripts/component_generator.py Button --dir src/components/ui
   ```

2. Generate a server component:
<<<<<<< HEAD
=======

>>>>>>> origin/main
   ```bash
   python scripts/component_generator.py ProductCard --type server
   ```

3. Generate with test and story files:
<<<<<<< HEAD
=======

>>>>>>> origin/main
   ```bash
   python scripts/component_generator.py UserProfile --with-test --with-story
   ```

4. Generate a custom hook:
   ```bash
   python scripts/component_generator.py FormValidation --type hook
   ```

### Generator Options

<<<<<<< HEAD
| Option | Description |
|--------|-------------|
| `--type client` | Client component with 'use client' (default) |
| `--type server` | Async server component |
| `--type hook` | Custom React hook |
| `--with-test` | Include test file |
| `--with-story` | Include Storybook story |
| `--flat` | Create in output dir without subdirectory |
| `--dry-run` | Preview without creating files |
=======
| Option          | Description                                  |
| --------------- | -------------------------------------------- |
| `--type client` | Client component with 'use client' (default) |
| `--type server` | Async server component                       |
| `--type hook`   | Custom React hook                            |
| `--with-test`   | Include test file                            |
| `--with-story`  | Include Storybook story                      |
| `--flat`        | Create in output dir without subdirectory    |
| `--dry-run`     | Preview without creating files               |
>>>>>>> origin/main

### Generated Component Example

```tsx
<<<<<<< HEAD
'use client';

import { useState } from 'react';
import { cn } from '@/lib/utils';
=======
"use client";

import { useState } from "react";
import { cn } from "@/lib/utils";
>>>>>>> origin/main

interface ButtonProps {
  className?: string;
  children?: React.ReactNode;
}

export function Button({ className, children }: ButtonProps) {
<<<<<<< HEAD
  return (
    <div className={cn('', className)}>
      {children}
    </div>
  );
=======
  return <div className={cn("", className)}>{children}</div>;
>>>>>>> origin/main
}
```

---

## Bundle Analysis

Analyze package.json and project structure for bundle optimization opportunities.

### Workflow: Optimize Bundle Size

1. Run the analyzer on your project:
<<<<<<< HEAD
=======

>>>>>>> origin/main
   ```bash
   python scripts/bundle_analyzer.py /path/to/project
   ```

2. Review the health score and issues:
<<<<<<< HEAD
=======

>>>>>>> origin/main
   ```
   Bundle Health Score: 75/100 (C)

   HEAVY DEPENDENCIES:
     moment (290KB)
       Alternative: date-fns (12KB) or dayjs (2KB)

     lodash (71KB)
       Alternative: lodash-es with tree-shaking
   ```

3. Apply the recommended fixes by replacing heavy dependencies.

4. Re-run with verbose mode to check import patterns:
   ```bash
   python scripts/bundle_analyzer.py . --verbose
   ```

### Bundle Score Interpretation

<<<<<<< HEAD
| Score | Grade | Action |
|-------|-------|--------|
| 90-100 | A | Bundle is well-optimized |
| 80-89 | B | Minor optimizations available |
| 70-79 | C | Replace heavy dependencies |
| 60-69 | D | Multiple issues need attention |
| 0-59 | F | Critical bundle size problems |
=======
| Score  | Grade | Action                         |
| ------ | ----- | ------------------------------ |
| 90-100 | A     | Bundle is well-optimized       |
| 80-89  | B     | Minor optimizations available  |
| 70-79  | C     | Replace heavy dependencies     |
| 60-69  | D     | Multiple issues need attention |
| 0-59   | F     | Critical bundle size problems  |
>>>>>>> origin/main

### Heavy Dependencies Detected

The analyzer identifies these common heavy packages:

<<<<<<< HEAD
| Package | Size | Alternative |
|---------|------|-------------|
| moment | 290KB | date-fns (12KB) or dayjs (2KB) |
| lodash | 71KB | lodash-es with tree-shaking |
| axios | 14KB | Native fetch or ky (3KB) |
| jquery | 87KB | Native DOM APIs |
| @mui/material | Large | shadcn/ui or Radix UI |
=======
| Package       | Size  | Alternative                    |
| ------------- | ----- | ------------------------------ |
| moment        | 290KB | date-fns (12KB) or dayjs (2KB) |
| lodash        | 71KB  | lodash-es with tree-shaking    |
| axios         | 14KB  | Native fetch or ky (3KB)       |
| jquery        | 87KB  | Native DOM APIs                |
| @mui/material | Large | shadcn/ui or Radix UI          |
>>>>>>> origin/main

---

## React Patterns

Reference: `references/react_patterns.md`

### Compound Components

Share state between related components:

```tsx
const Tabs = ({ children }) => {
  const [active, setActive] = useState(0);
  return (
    <TabsContext.Provider value={{ active, setActive }}>
      {children}
    </TabsContext.Provider>
  );
};

Tabs.List = TabList;
Tabs.Panel = TabPanel;

// Usage
<Tabs>
  <Tabs.List>
    <Tabs.Tab>One</Tabs.Tab>
    <Tabs.Tab>Two</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel>Content 1</Tabs.Panel>
  <Tabs.Panel>Content 2</Tabs.Panel>
<<<<<<< HEAD
</Tabs>
=======
</Tabs>;
>>>>>>> origin/main
```

### Custom Hooks

Extract reusable logic:

```tsx
function useDebounce<T>(value: T, delay = 500): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// Usage
const debouncedSearch = useDebounce(searchTerm, 300);
```

### Render Props

Share rendering logic:

```tsx
function DataFetcher({ url, render }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
<<<<<<< HEAD
    fetch(url).then(r => r.json()).then(setData).finally(() => setLoading(false));
=======
    fetch(url)
      .then((r) => r.json())
      .then(setData)
      .finally(() => setLoading(false));
>>>>>>> origin/main
  }, [url]);

  return render({ data, loading });
}

// Usage
<DataFetcher
  url="/api/users"
  render={({ data, loading }) =>
    loading ? <Spinner /> : <UserList users={data} />
  }
<<<<<<< HEAD
/>
=======
/>;
>>>>>>> origin/main
```

---

## Next.js Optimization

Reference: `references/nextjs_optimization_guide.md`

### Server vs Client Components

Use Server Components by default. Add 'use client' only when you need:
<<<<<<< HEAD
=======

>>>>>>> origin/main
- Event handlers (onClick, onChange)
- State (useState, useReducer)
- Effects (useEffect)
- Browser APIs

```tsx
// Server Component (default) - no 'use client'
async function ProductPage({ params }) {
<<<<<<< HEAD
  const product = await getProduct(params.id);  // Server-side fetch
=======
  const product = await getProduct(params.id); // Server-side fetch
>>>>>>> origin/main

  return (
    <div>
      <h1>{product.name}</h1>
<<<<<<< HEAD
      <AddToCartButton productId={product.id} />  {/* Client component */}
=======
      <AddToCartButton productId={product.id} /> {/* Client component */}
>>>>>>> origin/main
    </div>
  );
}

// Client Component
<<<<<<< HEAD
'use client';
=======
("use client");
>>>>>>> origin/main
function AddToCartButton({ productId }) {
  const [adding, setAdding] = useState(false);
  return <button onClick={() => addToCart(productId)}>Add</button>;
}
```

### Image Optimization

```tsx
import Image from 'next/image';

// Above the fold - load immediately
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority
/>

// Responsive image with fill
<div className="relative aspect-video">
  <Image
    src="/product.jpg"
    alt="Product"
    fill
    sizes="(max-width: 768px) 100vw, 50vw"
    className="object-cover"
  />
</div>
```

### Data Fetching Patterns

```tsx
// Parallel fetching
async function Dashboard() {
<<<<<<< HEAD
  const [user, stats] = await Promise.all([
    getUser(),
    getStats()
  ]);
=======
  const [user, stats] = await Promise.all([getUser(), getStats()]);
>>>>>>> origin/main
  return <div>...</div>;
}

// Streaming with Suspense
async function ProductPage({ params }) {
  return (
    <div>
      <ProductDetails id={params.id} />
      <Suspense fallback={<ReviewsSkeleton />}>
        <Reviews productId={params.id} />
      </Suspense>
    </div>
  );
}
```

---

## Accessibility and Testing

Reference: `references/frontend_best_practices.md`

### Accessibility Checklist

1. **Semantic HTML**: Use proper elements (`<button>`, `<nav>`, `<main>`)
2. **Keyboard Navigation**: All interactive elements focusable
3. **ARIA Labels**: Provide labels for icons and complex widgets
4. **Color Contrast**: Minimum 4.5:1 for normal text
5. **Focus Indicators**: Visible focus states

```tsx
// Accessible button
<button
  type="button"
  aria-label="Close dialog"
  onClick={onClose}
  className="focus-visible:ring-2 focus-visible:ring-blue-500"
>
  <XIcon aria-hidden="true" />
</button>

// Skip link for keyboard users
<a href="#main-content" className="sr-only focus:not-sr-only">
  Skip to main content
</a>
```

### Testing Strategy

```tsx
// Component test with React Testing Library
<<<<<<< HEAD
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('button triggers action on click', async () => {
  const onClick = vi.fn();
  render(<Button onClick={onClick}>Click me</Button>);

  await userEvent.click(screen.getByRole('button'));
=======
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

test("button triggers action on click", async () => {
  const onClick = vi.fn();
  render(<Button onClick={onClick}>Click me</Button>);

  await userEvent.click(screen.getByRole("button"));
>>>>>>> origin/main
  expect(onClick).toHaveBeenCalledTimes(1);
});

// Test accessibility
<<<<<<< HEAD
test('dialog is accessible', async () => {
  render(<Dialog open={true} title="Confirm" />);

  expect(screen.getByRole('dialog')).toBeInTheDocument();
  expect(screen.getByRole('dialog')).toHaveAttribute('aria-labelledby');
=======
test("dialog is accessible", async () => {
  render(<Dialog open={true} title="Confirm" />);

  expect(screen.getByRole("dialog")).toBeInTheDocument();
  expect(screen.getByRole("dialog")).toHaveAttribute("aria-labelledby");
>>>>>>> origin/main
});
```

---

## Quick Reference

### Common Next.js Config

```js
// next.config.js
const nextConfig = {
  images: {
<<<<<<< HEAD
    remotePatterns: [{ hostname: 'cdn.example.com' }],
    formats: ['image/avif', 'image/webp'],
  },
  experimental: {
    optimizePackageImports: ['lucide-react', '@heroicons/react'],
=======
    remotePatterns: [{ hostname: "cdn.example.com" }],
    formats: ["image/avif", "image/webp"],
  },
  experimental: {
    optimizePackageImports: ["lucide-react", "@heroicons/react"],
>>>>>>> origin/main
  },
};
```

### Tailwind CSS Utilities

```tsx
// Conditional classes with cn()
<<<<<<< HEAD
import { cn } from '@/lib/utils';

<button className={cn(
  'px-4 py-2 rounded',
  variant === 'primary' && 'bg-blue-500 text-white',
  disabled && 'opacity-50 cursor-not-allowed'
)} />
=======
import { cn } from "@/lib/utils";

<button
  className={cn(
    "px-4 py-2 rounded",
    variant === "primary" && "bg-blue-500 text-white",
    disabled && "opacity-50 cursor-not-allowed",
  )}
/>;
>>>>>>> origin/main
```

### TypeScript Patterns

```tsx
// Props with children
interface CardProps {
  className?: string;
  children: React.ReactNode;
}

// Generic component
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
}

function List<T>({ items, renderItem }: ListProps<T>) {
  return <ul>{items.map(renderItem)}</ul>;
}
```

---

## Resources

- React Patterns: `references/react_patterns.md`
- Next.js Optimization: `references/nextjs_optimization_guide.md`
- Best Practices: `references/frontend_best_practices.md`
<<<<<<< HEAD

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.
=======
>>>>>>> origin/main
