import os
import json
import pathlib
import shutil
import re
import sys
from collections.abc import Mapping
from datetime import date, datetime

import yaml
from _project_paths import find_repo_root
from plugin_compatibility import build_report as build_plugin_compatibility_report
from plugin_compatibility import compatibility_by_path as plugin_compatibility_by_path

# Ensure UTF-8 output for Windows compatibility
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


CATEGORY_RULES = [
    {
        "name": "security",
        "keywords": [
            "security", "auth", "authentication", "authorization", "oauth", "jwt",
            "cryptography", "encryption", "vulnerability", "threat", "pentest",
            "xss", "sqli", "gdpr", "pci", "compliance",
        ],
    },
    {
        "name": "testing",
        "keywords": [
            "test", "testing", "tdd", "qa", "e2e", "playwright", "cypress",
            "pytest", "jest", "benchmark", "evaluation", "end to end",
        ],
        "strong_keywords": ["playwright", "cypress", "pytest", "jest", "e2e", "end to end"],
    },
    {
        "name": "automation",
        "keywords": [
            "automation", "workflow", "trigger", "integration", "slack",
            "airtable", "calendar", "gmail", "google", "hubspot", "notion",
            "zendesk", "stripe", "shopify", "sendgrid", "clickup", "n8n",
            "zapier", "make", "zoom",
        ],
    },
    {
        "name": "devops",
        "keywords": [
            "docker", "kubernetes", "k8s", "helm", "terraform", "deploy",
            "deployment", "cicd", "gitops", "observability", "monitoring",
            "grafana", "prometheus", "incident", "sre", "tracing",
        ],
    },
    {
        "name": "cloud",
        "keywords": [
            "aws", "azure", "gcp", "cloud", "serverless", "lambda", "storage",
            "functions", "cdn", "azure", "azd",
        ],
    },
    {
        "name": "database",
        "keywords": [
            "database", "sql", "postgres", "postgresql", "mysql", "mongodb",
            "redis", "orm", "schema", "migration", "query", "prisma",
        ],
    },
    {
        "name": "ai-ml",
        "keywords": [
            "ai", "ml", "llm", "agent", "agents", "gpt", "embedding",
            "vector", "rag", "prompt", "model", "training", "inference",
            "pytorch", "tensorflow", "hugging", "openai",
        ],
    },
    {
        "name": "mobile",
        "keywords": [
            "mobile", "android", "ios", "swift", "swiftui", "kotlin",
            "flutter", "expo", "react native", "app store", "play store",
            "jetpack compose",
        ],
    },
    {
        "name": "game-development",
        "keywords": [
            "game", "unity", "unreal", "godot", "threejs", "3d", "2d",
            "shader", "rendering", "webgl", "physics",
        ],
    },
    {
        "name": "web-development",
        "keywords": [
            "web", "frontend", "react", "nextjs", "vue", "angular", "svelte",
            "tailwind", "css", "html", "browser", "extension", "component",
            "ui", "ux", "javascript", "typescript",
        ],
    },
    {
        "name": "backend",
        "keywords": [
            "backend", "api", "fastapi", "django", "flask", "express",
            "node", "server", "middleware", "graphql", "rest",
        ],
    },
    {
        "name": "data-science",
        "keywords": [
            "data", "analytics", "pandas", "numpy", "statistics",
            "matplotlib", "plotly", "seaborn", "scipy", "notebook",
        ],
    },
    {
        "name": "content",
        "keywords": [
            "content", "copy", "copywriting", "writing", "documentation",
            "transcription", "transcribe", "seo", "blog", "markdown",
        ],
    },
    {
        "name": "education",
        "keywords": [
            "education", "student", "syllabus", "exam", "study",
            "teacher", "curriculum", "classroom", "school",
            "examprep", "roadmap", "academic", "university",
        ],
    },
    {
        "name": "business",
        "keywords": [
            "business", "product", "market", "sales", "finance", "startup",
            "legal", "customer", "competitive", "pricing", "kpi",
        ],
    },
    {
        "name": "architecture",
        "keywords": [
            "architecture", "adr", "microservices", "ddd", "domain",
            "cqrs", "saga", "patterns",
        ],
    },
]

FAMILY_CATEGORY_RULES = [
    ("azure-", "cloud"),
    ("aws-", "cloud"),
    ("gcp-", "cloud"),
    ("apify-", "automation"),
    ("google-", "automation"),
    ("n8n-", "automation"),
    ("makepad-", "development"),
    ("robius-", "development"),
    ("avalonia-", "development"),
    ("hig-", "development"),
    ("fp-", "development"),
    ("fp-ts-", "development"),
    ("threejs-", "web-development"),
    ("react-", "web-development"),
    ("vue-", "web-development"),
    ("angular-", "web-development"),
    ("browser-", "web-development"),
    ("expo-", "mobile"),
    ("swiftui-", "mobile"),
    ("android-", "mobile"),
    ("ios-", "mobile"),
    ("hugging-face-", "ai-ml"),
    ("agent-", "ai-ml"),
    ("agents-", "ai-ml"),
    ("ai-", "ai-ml"),
    ("claude-", "ai-ml"),
    ("context-", "ai-ml"),
    ("fal-", "ai-ml"),
    ("yann-", "ai-ml"),
    ("llm-", "ai-ml"),
    ("rag-", "ai-ml"),
    ("embedding-", "ai-ml"),
    ("odoo-", "business"),
    ("product-", "business"),
    ("data-", "data-science"),
    ("wiki-", "content"),
    ("documentation-", "content"),
    ("copy", "content"),
    ("audio-", "content"),
    ("video-", "content"),
    ("api-", "backend"),
    ("django-", "backend"),
    ("fastapi-", "backend"),
    ("backend-", "backend"),
    ("python-", "development"),
    ("bash-", "development"),
    ("code-", "development"),
    ("codebase-", "development"),
    ("error-", "development"),
    ("framework-", "development"),
    ("debugging-", "development"),
    ("javascript-", "development"),
    ("go-", "development"),
    ("performance-", "development"),
    ("dbos-", "development"),
    ("conductor-", "workflow"),
    ("workflow-", "workflow"),
    ("create-", "workflow"),
    ("git-", "workflow"),
    ("github-", "workflow"),
    ("gitlab-", "workflow"),
    ("skill-", "meta"),
    ("cc-skill-", "meta"),
    ("tdd-", "testing"),
    ("test-", "testing"),
    ("security-", "security"),
    ("database-", "database"),
    ("c4-", "architecture"),
    ("deployment-", "devops"),
    ("incident-", "devops"),
    ("terraform-", "devops"),
]

CURATED_CATEGORY_OVERRIDES = {
    "ai-agents-architect": "ai-agents",
    "agent-evaluation": "ai-agents",
    "agent-manager-skill": "ai-agents",
    "langgraph": "ai-agents",
    "multi-agent-patterns": "ai-agents",
    "pydantic-ai": "ai-agents",
    "plaid-fintech": "api-integration",
    "stripe-integration": "api-integration",
    "paypal-integration": "api-integration",
    "hubspot-integration": "api-integration",
    "twilio-communications": "api-integration",
    "pakistan-payments-stack": "api-integration",
    "javascript-typescript-typescript-scaffold": "app-builder",
    "fastapi-templates": "app-builder",
    "frontend-mobile-development-component-scaffold": "app-builder",
    "templates": "app-builder",
    "blockchain-developer": "blockchain",
    "crypto-bd-agent": "blockchain",
    "defi-protocol-templates": "blockchain",
    "goldrush-api": "blockchain",
    "lightning-architecture-review": "blockchain",
    "lightning-channel-factories": "blockchain",
    "lightning-factory-explainer": "blockchain",
    "web3-testing": "blockchain",
    "javascript-pro": "code",
    "python-pro": "code",
    "typescript-pro": "code",
    "golang-pro": "code",
    "rust-pro": "code",
    "uncle-bob-craft": "code-quality",
    "clean-code": "code-quality",
    "kaizen": "code-quality",
    "code-review-checklist": "code-quality",
    "codebase-cleanup-tech-debt": "code-quality",
    "code-refactoring-refactor-clean": "code-quality",
    "comprehensive-review-full-review": "code-quality",
    "comprehensive-review-pr-enhance": "code-quality",
    "data-engineer": "data",
    "dbt-transformation-patterns": "data",
    "analytics-tracking": "data",
    "sql-pro": "data",
    "web-scraper": "data",
    "x-twitter-scraper": "data",
    "ai-engineering-toolkit": "data-ai",
    "embedding-strategies": "data-ai",
    "llm-app-patterns": "data-ai",
    "local-llm-expert": "data-ai",
    "rag-engineer": "data-ai",
    "seek-and-analyze-video": "data-ai",
    "vector-database-engineer": "data-ai",
    "database-admin": "database-processing",
    "database-architect": "database-processing",
    "database-design": "database-processing",
    "database-optimizer": "database-processing",
    "base": "database-processing",
    "using-neon": "database-processing",
    "bug-hunter": "development-and-testing",
    "debugging-strategies": "development-and-testing",
    "openclaw-github-repo-commander": "development-and-testing",
    "systematic-debugging": "development-and-testing",
    "test-fixing": "development-and-testing",
    "antigravity-design-expert": "design",
    "design-md": "design",
    "design-orchestration": "design",
    "design-spells": "design",
    "stitch-ui-design": "design",
    "web-design-guidelines": "design",
    "docx-official": "document-processing",
    "doc-coauthoring": "document-processing",
    "pdf": "document-processing",
    "pdf-official": "document-processing",
    "writer": "document-processing",
    "landing-page-generator": "front-end",
    "frontend-design": "front-end",
    "frontend-developer": "front-end",
    "frontend-dev-guidelines": "front-end",
    "ui-ux-pro-max": "front-end",
    "astro": "frontend",
    "nextjs-best-practices": "frontend",
    "react-patterns": "frontend",
    "sveltekit": "frontend",
    "tailwind-patterns": "frontend",
    "django-pro": "framework",
    "fastapi-pro": "framework",
    "nestjs-expert": "framework",
    "nextjs-app-router-patterns": "framework",
    "trpc-fullstack": "framework",
    "typescript-expert": "framework",
    "algorithmic-art": "graphics-processing",
    "canvas-design": "graphics-processing",
    "draw": "graphics-processing",
    "image-studio": "graphics-processing",
    "imagen": "graphics-processing",
    "laravel-expert": "framework",
    "laravel-security-audit": "security",
    "advogado-criminal": "legal",
    "advogado-especialista": "legal",
    "customs-trade-compliance": "legal",
    "employment-contract-templates": "legal",
    "legal-advisor": "legal",
    "lex": "legal",
    "app-store-optimization": "marketing",
    "brand-guidelines": "marketing",
    "brand-guidelines-anthropic": "marketing",
    "brand-guidelines-community": "marketing",
    "content-creator": "marketing",
    "copy-editing": "marketing",
    "copywriting": "marketing",
    "email-sequence": "marketing",
    "free-tool-strategy": "marketing",
    "growth-engine": "marketing",
    "instagram": "marketing",
    "instagram-automation": "marketing",
    "launch-strategy": "marketing",
    "linkedin-automation": "marketing",
    "linkedin-cli": "marketing",
    "marketing-ideas": "marketing",
    "marketing-psychology": "marketing",
    "programmatic-seo": "marketing",
    "social-content": "marketing",
    "social-orchestrator": "marketing",
    "remotion-best-practices": "media",
    "sora": "media",
    "videodb": "media",
    "videodb-skills": "media",
    "agent-memory-systems": "memory",
    "context-window-management": "memory",
    "conversation-memory": "memory",
    "hierarchical-agent-memory": "memory",
    "memory-systems": "memory",
    "recallmax": "memory",
    "memory-forensics": "security",
    "memory-safety-patterns": "development",
    "m365-agents-dotnet": "ai-agents",
    "m365-agents-ts": "ai-agents",
    "hosted-agents": "ai-agents",
    "hosted-agents-v2-py": "ai-agents",
    "multi-advisor": "ai-agents",
    "multi-platform-apps-multi-platform": "development",
    "mobile-design": "mobile",
    "mobile-security-coder": "mobile",
    "blueprint": "planning",
    "concise-planning": "planning",
    "planning-with-files": "planning",
    "track-management": "planning",
    "google-slides-automation": "presentation-processing",
    "frontend-slides": "presentation-processing",
    "impress": "presentation-processing",
    "pptx-official": "presentation-processing",
    "file-organizer": "productivity",
    "google-calendar-automation": "productivity",
    "interview-coach": "productivity",
    "office-productivity": "productivity",
    "risk-manager": "business",
    "risk-metrics-calculation": "business",
    "github-issue-creator": "project-management",
    "linear-claude-skill": "project-management",
    "progressive-estimation": "project-management",
    "team-collaboration-issue": "project-management",
    "team-collaboration-standup-notes": "project-management",
    "freshservice-automation": "project-management",
    "wrike-automation": "project-management",
    "distributed-debugging-debug-trace": "reliability",
    "distributed-tracing": "reliability",
    "incident-responder": "reliability",
    "observability-engineer": "reliability",
    "postmortem-writing": "reliability",
    "slo-implementation": "reliability",
    "tool-use-guardian": "reliability",
    "calc": "spreadsheet-processing",
    "google-sheets-automation": "spreadsheet-processing",
    "googlesheets-automation": "spreadsheet-processing",
    "xlsx-official": "spreadsheet-processing",
    "awt-e2e-testing": "test-automation",
    "browser-automation": "test-automation",
    "e2e-testing-patterns": "test-automation",
    "go-playwright": "test-automation",
    "playwright-java": "test-automation",
    "playwright-skill": "test-automation",
    "test-automator": "test-automation",
    "webapp-testing": "test-automation",
    "ffuf-claude-skill": "security",
    "ffuf-web-fuzzing": "security",
    "file-path-traversal": "security",
    "file-uploads": "security",
    "semgrep-rule-creator": "security",
    "semgrep-rule-variant-creator": "security",
    "seo-audit": "content",
    "seo-forensic-incident-response": "content",
    "fixing-accessibility": "front-end",
    "fixing-metadata": "front-end",
    "fixing-motion-performance": "front-end",
    "internal-comms-anthropic": "content",
    "internal-comms-community": "content",
    "leiloeiro-avaliacao": "leiloeiro",
    "leiloeiro-edital": "leiloeiro",
    "leiloeiro-ia": "leiloeiro",
    "leiloeiro-juridico": "leiloeiro",
    "leiloeiro-mercado": "leiloeiro",
    "leiloeiro-risco": "leiloeiro",
    "linux-privilege-escalation": "security",
    "linux-shell-scripting": "development",
    "mcp-builder": "ai-agents",
    "mcp-builder-ms": "ai-agents",
    "monorepo-architect": "development",
    "monorepo-management": "development",
    "pentest-checklist": "security",
    "pentest-commands": "security",
    "salesforce-automation": "api-integration",
    "salesforce-development": "api-integration",
    "segment-automation": "data",
    "segment-cdp": "data",
    "senior-architect": "development",
    "senior-fullstack": "development",
    "shopify-apps": "api-integration",
    "shopify-development": "api-integration",
    "sred-project-organizer": "project-management",
    "sred-work-summary": "project-management",
    "startup-business-analyst-financial-projections": "business",
    "startup-financial-modeling": "business",
    "telegram-automation": "api-integration",
    "telegram-bot-builder": "api-integration",
    "temporal-golang-pro": "workflow",
    "temporal-python-pro": "workflow",
    "using-git-worktrees": "development",
    "using-superpowers": "meta",
    "varlock": "security",
    "varlock-claude-skill": "security",
    "vexor": "development",
    "vexor-cli": "development",
    "audio-transcriber": "voice-agents",
    "fal-audio": "voice-agents",
    "pipecat-friday-agent": "voice-agents",
    "3d-web-experience": "design",
    "ab-test-setup": "marketing",
    "acceptance-orchestrator": "workflow",
    "accessibility-compliance-accessibility-audit": "design",
    "active-directory-attacks": "security",
    "activecampaign-automation": "marketing",
    "alpha-vantage": "data",
    "amplitude-automation": "data",
    "analytics-product": "data",
    "analyze-project": "meta",
    "antigravity-workflows": "workflow",
    "anti-reversing-techniques": "security",
    "arm-cortex-expert": "development",
    "asana-automation": "project-management",
    "ask-questions-if-underspecified": "workflow",
    "audit-context-building": "meta",
    "basecamp-automation": "project-management",
    "bazel-build-optimization": "development",
    "behavioral-modes": "meta",
    "bitbucket-automation": "workflow",
    "blog-writing-guide": "content",
    "box-automation": "productivity",
    "brevo-automation": "marketing",
    "broken-authentication": "security",
    "building-native-ui": "mobile",
    "bullmq-specialist": "framework",
    "burp-suite-testing": "security",
    "business-analyst": "business",
    "busybox-on-windows": "development",
    "c-pro": "code",
    "cal-com-automation": "productivity",
    "calendly-automation": "productivity",
    "canva-automation": "design",
    "carrier-relationship-management": "business",
    "changelog-automation": "workflow",
    "cloudflare-workers-expert": "framework",
    "closed-loop-delivery": "workflow",
    "commit": "workflow",
    "confluence-automation": "project-management",
    "constant-time-analysis": "security",
    "context7-auto-research": "meta",
    "convex": "framework",
    "convertkit-automation": "marketing",
    "cpp-pro": "code",
    "cred-omega": "security",
    "csharp-pro": "code",
    "datadog-automation": "reliability",
    "dependency-upgrade": "development",
    "differential-review": "security",
    "discord-automation": "api-integration",
    "docusign-automation": "productivity",
    "dotnet-architect": "development",
    "dropbox-automation": "productivity",
    "dx-optimizer": "development",
    "elixir-pro": "code",
    "electron-development": "development",
    "energy-procurement": "business",
    "environment-setup-guide": "development",
    "ethical-hacking-methodology": "security",
    "executing-plans": "workflow",
    "fda-food-safety-auditor": "legal",
    "fda-medtech-compliance-auditor": "legal",
    "figma-automation": "design",
    "filesystem-context": "meta",
    "flutter-expert": "mobile",
    "gha-security-review": "security",
    "gh-review-requests": "workflow",
    "gmail-automation": "productivity",
    "haskell-pro": "code",
    "hr-pro": "business",
    "inngest": "workflow",
    "inventory-demand-planning": "business",
    "iterate-pr": "workflow",
    "java-pro": "code",
    "jira-automation": "project-management",
    "klaviyo-automation": "marketing",
    "linear-automation": "project-management",
    "mailchimp-automation": "marketing",
    "microsoft-teams-automation": "api-integration",
    "miro-automation": "project-management",
    "mixpanel-automation": "data",
    "ml-pipeline-workflow": "workflow",
    "monday-automation": "project-management",
    "on-call-handoff-patterns": "reliability",
    "one-drive-automation": "productivity",
    "pagerduty-automation": "reliability",
    "php-pro": "code",
    "pipedrive-automation": "business",
    "plan-writing": "planning",
    "postmark-automation": "api-integration",
    "posthog-automation": "data",
    "pr-writer": "workflow",
    "privacy-by-design": "security",
    "receiving-code-review": "workflow",
    "reddit-automation": "marketing",
    "requesting-code-review": "workflow",
    "ruby-pro": "code",
    "scala-pro": "code",
    "sentry-automation": "reliability",
    "service-mesh-expert": "reliability",
    "shadcn": "framework",
    "square-automation": "api-integration",
    "subagent-driven-development": "workflow",
    "tanstack-query-expert": "framework",
    "tiktok-automation": "marketing",
    "todoist-automation": "project-management",
    "trello-automation": "project-management",
    "trigger-dev": "workflow",
    "twitter-automation": "marketing",
    "ui-visual-validator": "design",
    "unreal-engine-cpp-pro": "code",
    "uv-package-manager": "development",
    "webflow-automation": "design",
    "whatsapp-automation": "api-integration",
    "writing-plans": "planning",
    "youtube-automation": "marketing",
    "zod-validation-expert": "framework",
    "zoho-crm-automation": "business",
    "address-github-comments": "workflow",
    "airflow-dag-patterns": "workflow",
    "algolia-search": "api-integration",
    "android_ui_verification": "test-automation",
    "application-performance-performance-optimization": "reliability",
    "architect-review": "architecture",
    "astropy": "science",
    "async-python-patterns": "development",
    "auri-core": "voice-agents",
    "binary-analysis-patterns": "security",
    "biopython": "science",
    "build": "workflow",
    "burpsuite-project-parser": "security",
    "cdk-patterns": "cloud",
    "chat-widget": "front-end",
    "chrome-extension-developer": "front-end",
    "cirq": "science",
    "citation-management": "content",
    "cloudformation-best-practices": "cloud",
    "computer-vision-expert": "ai-ml",
    "cqrs-implementation": "architecture",
    "ddd-strategic-design": "architecture",
    "deep-research": "ai-ml",
    "dispatching-parallel-agents": "ai-agents",
    "emergency-card": "health",
    "evaluation": "ai-ml",
    "event-store-design": "architecture",
    "exa-search": "data-ai",
    "examprep-ai": "education",
    "explain-like-socrates": "content",
    "family-health-analyzer": "health",
    "find-bugs": "code-quality",
    "finishing-a-development-branch": "workflow",
    "firebase": "cloud",
    "firmware-analyst": "security",
    "fitness-analyzer": "health",
    "fix-review": "code-quality",
    "food-database-query": "health",
    "freshdesk-automation": "automation",
    "form-cro": "marketing",
    "full-stack-orchestration-full-stack-feature": "workflow",
    "game-development": "game-development",
    "gdpr-data-handling": "security",
    "gemini-api-dev": "ai-ml",
    "geo-fundamentals": "marketing",
    "goal-analyzer": "health",
    "graphql-architect": "architecture",
    "health-trend-analyzer": "health",
    "helpdesk-automation": "automation",
    "html-injection-testing": "security",
    "hybrid-cloud-networking": "cloud",
    "i18n-localization": "development",
    "idor-testing": "security",
    "interactive-portfolio": "front-end",
    "intercom-automation": "automation",
    "issues": "workflow",
    "keyword-extractor": "marketing",
    "legacy-modernizer": "development",
    "lint-and-validate": "workflow",
    "local-legal-seo-audit": "marketing",
    "malware-analyst": "security",
    "mental-health-analyzer": "health",
    "metasploit-framework": "security",
    "micro-saas-launcher": "business",
    "modern-javascript-patterns": "development",
    "monetization": "business",
    "mtls-configuration": "security",
    "native-data-fetching": "development",
    "networkx": "science",
    "notion-template-business": "business",
    "nutrition-analyzer": "health",
    "nx-workspace-patterns": "development",
    "onboarding-cro": "marketing",
    "occupational-health-analyzer": "health",
    "openapi-spec-generation": "api-integration",
    "oral-health-analyzer": "health",
    "page-cro": "marketing",
    "paid-ads": "marketing",
    "parallel-agents": "ai-agents",
    "payment-integration": "api-integration",
    "paywall-upgrade-cro": "marketing",
    "popup-cro": "marketing",
    "privilege-escalation-methods": "security",
    "production-scheduling": "business",
    "professional-proofreader": "content",
    "progressive-web-app": "front-end",
    "projection-patterns": "architecture",
    "protocol-reverse-engineering": "security",
    "pydantic-models-py": "development",
    "pypict-skill": "testing",
    "qiskit": "science",
    "quality-nonconformance": "business",
    "readme": "content",
    "red-team-tactics": "security",
    "reference-builder": "content",
    "referral-program": "marketing",
    "rehabilitation-analyzer": "health",
    "render-automation": "automation",
    "returns-reverse-logistics": "business",
    "reverse-engineer": "security",
    "rust-async-patterns": "development",
    "saas-mvp-launcher": "business",
    "sast-configuration": "security",
    "scanpy": "science",
    "schema-markup": "marketing",
    "scientific-writing": "content",
    "screen-reader-testing": "testing",
    "screenshots": "marketing",
    "scroll-experience": "front-end",
    "search-specialist": "content",
    "seaborn": "science",
    "secrets-management": "security",
    "shodan-reconnaissance": "security",
    "signup-flow-cro": "marketing",
    "similarity-search-patterns": "data-ai",
    "skin-health-analyzer": "health",
    "sleep-analyzer": "health",
    "spec-to-code-compliance": "code-quality",
    "sql-injection-testing": "security",
    "ssh-penetration-testing": "security",
    "systems-programming-rust-project": "development",
    "tcm-constitution-analyzer": "health",
    "team-composition-analysis": "business",
    "travel-health-analyzer": "health",
    "vibe-code-auditor": "code-quality",
    "vibers-code-review": "code-quality",
    "voice-ai-development": "voice-agents",
    "weightloss-analyzer": "health",
    "windows-privilege-escalation": "security",
    "wordpress-penetration-testing": "security",
    "xss-html-injection": "security",
    "backtesting-frameworks": "business",
    "bamboohr-automation": "business",
    "beautiful-prose": "content",
    "clarity-gate": "data-ai",
    "codex-review": "code-quality",
    "customer-support": "business",
    "debugger": "development-and-testing",
    "devcontainer-setup": "development",
    "diary": "meta",
    "dwarf-expert": "development",
    "firecrawl-scraper": "data",
    "godot-4-migration": "game-development",
    "grpc-golang": "development",
    "istio-traffic-management": "cloud",
    "julia-pro": "code",
    "kotlin-coroutines-expert": "development",
    "matplotlib": "science",
    "mermaid-expert": "content",
    "minecraft-bukkit-pro": "game-development",
    "moodle-external-api-development": "api-integration",
    "nanobanana-ppt-skills": "presentation-processing",
    "notebooklm": "data-ai",
    "prompt-library": "content",
    "quant-analyst": "business",
    "remotion": "media",
    "server-management": "reliability",
    "sexual-health-analyzer": "health",
    "shellcheck-configuration": "code-quality",
    "slack-bot-builder": "api-integration",
    "software-architecture": "architecture",
    "spark-optimization": "data",
    "statsmodels": "science",
    "stability-ai": "media",
    "sympy": "science",
    "task-intelligence": "workflow",
    "tavily-web": "data-ai",
    "theme-factory": "design",
    "turborepo-caching": "development",
    "tutorial-engineer": "content",
    "typescript-advanced-types": "code",
    "unity-ecs-patterns": "game-development",
    "unsplash-integration": "api-integration",
    "upgrading-expo": "mobile",
    "upstash-qstash": "workflow",
    "vector-index-tuning": "data-ai",
    "verification-before-completion": "workflow",
    "viral-generator-builder": "marketing",
    "vizcom": "design",
    "wcag-audit-patterns": "design",
    "web-performance-optimization": "front-end",
    "wireshark-analysis": "security",
    "x-article-publisher-skill": "marketing",
    "zeroize-audit": "security",
    "zustand-store-ts": "frontend",
}


# --- 10-bucket taxonomy (confirmed 2026-07-23) ------------------------------
# Every skill must land in exactly one of these 10 buckets. TAXONOMY_MAP
# translates every legacy category value (the ~97 fine-grained categories
# produced by CATEGORY_RULES / FAMILY_CATEGORY_RULES / CURATED_CATEGORY_OVERRIDES
# above, plus any explicit frontmatter `category:` value) into its bucket.
# Skills that resolve to no legacy category at all ("uncategorized") are
# instead classified directly into a bucket by NEW_TAXONOMY_RULES /
# infer_new_taxonomy_category() below, so "uncategorized" should no longer
# occur in the generated index.
NEW_TAXONOMY_BUCKETS = [
    "AI & Agents",
    "Desarrollo de Software",
    "Cloud, DevOps & Automatización",
    "Seguridad",
    "Testing & Calidad",
    "Diseño & Contenido",
    "Negocio & Marketing",
    "Gestión de Proyectos & Equipos",
    "Verticales Especializados",
    "Meta & Productividad Personal",
]

TAXONOMY_MAP = {
    # AI & Agents
    "ai-ml": "AI & Agents",
    "ai-agents": "AI & Agents",
    "data-ai": "AI & Agents",
    "data": "AI & Agents",
    "data-science": "AI & Agents",
    "ai-research": "AI & Agents",
    "prompt-engineering": "AI & Agents",
    "ml-ops": "AI & Agents",
    "mcp": "AI & Agents",
    "memory": "AI & Agents",
    "agent-behavior": "AI & Agents",
    "agent-orchestration": "AI & Agents",
    "orchestration": "AI & Agents",
    # Desarrollo de Software
    "development": "Desarrollo de Software",
    "backend": "Desarrollo de Software",
    "frontend": "Desarrollo de Software",
    "front-end": "Desarrollo de Software",
    "web-development": "Desarrollo de Software",
    "mobile": "Desarrollo de Software",
    "code": "Desarrollo de Software",
    "coding": "Desarrollo de Software",
    "framework": "Desarrollo de Software",
    "api-integration": "Desarrollo de Software",
    "architecture": "Desarrollo de Software",
    "database": "Desarrollo de Software",
    "app-builder": "Desarrollo de Software",
    "developer-tools": "Desarrollo de Software",
    "core-dev": "Desarrollo de Software",
    "fullstack": "Desarrollo de Software",
    "engineering": "Desarrollo de Software",
    "tools": "Desarrollo de Software",
    "database-processing": "Desarrollo de Software",
    "development-and-testing": "Desarrollo de Software",
    "super-code": "Desarrollo de Software",
    # Cloud, DevOps & Automatización
    "cloud": "Cloud, DevOps & Automatización",
    "devops": "Cloud, DevOps & Automatización",
    "automation": "Cloud, DevOps & Automatización",
    "workflow": "Cloud, DevOps & Automatización",
    "granular-workflow-bundle": "Cloud, DevOps & Automatización",
    "workflow-bundle": "Cloud, DevOps & Automatización",
    "reliability": "Cloud, DevOps & Automatización",
    "browser-automation": "Cloud, DevOps & Automatización",
    "engineering-team": "Cloud, DevOps & Automatización",
    # Seguridad
    "security": "Seguridad",
    # Testing & Calidad
    "testing": "Testing & Calidad",
    "test-automation": "Testing & Calidad",
    "code-quality": "Testing & Calidad",
    "quality": "Testing & Calidad",
    "tool-quality": "Testing & Calidad",
    "engineering / code quality": "Testing & Calidad",
    "ai-testing": "Testing & Calidad",
    # Diseño & Contenido
    "content": "Diseño & Contenido",
    "design": "Diseño & Contenido",
    "media": "Diseño & Contenido",
    "graphics-processing": "Diseño & Contenido",
    "voice-agents": "Diseño & Contenido",
    "document-processing": "Diseño & Contenido",
    "presentation-processing": "Diseño & Contenido",
    "spreadsheet-processing": "Diseño & Contenido",
    "media-processing": "Diseño & Contenido",
    "video": "Diseño & Contenido",
    "creative": "Diseño & Contenido",
    "writing": "Diseño & Contenido",
    "seo": "Diseño & Contenido",
    "documentacion-de-codigo": "Diseño & Contenido",
    # Negocio & Marketing
    "business": "Negocio & Marketing",
    "marketing": "Negocio & Marketing",
    "marketing-skill": "Negocio & Marketing",
    "business-growth": "Negocio & Marketing",
    "growth": "Negocio & Marketing",
    "business-strategy": "Negocio & Marketing",
    "consulting": "Negocio & Marketing",
    "ecommerce": "Negocio & Marketing",
    "finance": "Negocio & Marketing",
    "c-level-advisor": "Negocio & Marketing",
    # Gestión de Proyectos & Equipos
    "project-management": "Gestión de Proyectos & Equipos",
    "product-management": "Gestión de Proyectos & Equipos",
    "planning": "Gestión de Proyectos & Equipos",
    "collaboration": "Gestión de Proyectos & Equipos",
    # Verticales Especializados
    "health": "Verticales Especializados",
    "legal": "Verticales Especializados",
    "blockchain": "Verticales Especializados",
    "education": "Verticales Especializados",
    "science": "Verticales Especializados",
    "game-development": "Verticales Especializados",
    "leiloeiro": "Verticales Especializados",
    "andruia": "Verticales Especializados",
    "research": "Verticales Especializados",
    # Meta & Productividad Personal
    "meta": "Meta & Productividad Personal",
    "productivity": "Meta & Productividad Personal",
    "skill-authoring": "Meta & Productividad Personal",
    "context-optimization": "Meta & Productividad Personal",
    "general": "Meta & Productividad Personal",
    "claude.ai": "Meta & Productividad Personal",
    "antigravity-awesome-skills": "Meta & Productividad Personal",
    "knowledge-management": "Meta & Productividad Personal",
    "personal-development": "Meta & Productividad Personal",
}

# --- Direct classifier for skills that have NO legacy category at all -------
# (no frontmatter `category:`, no folder-derived category, and the legacy
# infer_category() keyword rules below found nothing confident either).
# These previously fell through to "uncategorized". Instead of leaving them
# unclassified, score name+id+description directly against the 10 buckets.
# Seed vocabulary = the legacy category names that feed each bucket (see
# TAXONOMY_MAP above) plus obvious domain terms. Order below = priority used
# to break ties, most specific/narrow bucket first so ambiguous skills don't
# default into the broad "Meta & Productividad Personal" catch-all.
NEW_TAXONOMY_BUCKET_PRIORITY = [
    "Seguridad",
    "Testing & Calidad",
    "Verticales Especializados",
    "Diseño & Contenido",
    "Negocio & Marketing",
    "Gestión de Proyectos & Equipos",
    "Cloud, DevOps & Automatización",
    "AI & Agents",
    "Desarrollo de Software",
    "Meta & Productividad Personal",
]

NEW_TAXONOMY_RULES = {
    "Seguridad": {
        "strong": [
            "security", "vulnerability", "pentest", "penetration", "exploit",
            "malware", "cve", "threat", "attack", "auth", "authentication",
            "authorization", "encryption", "cryptograph", "oauth", "jwt",
            "xss", "sqli", "injection", "firewall", "compliance audit",
            "privilege escalation", "reverse engineer", "ransomware",
            "phishing", "zero day", "secrets", "hardening", "ciso",
            "red team", "blue team", "forensics", "reconnaissance",
        ],
        "weak": ["risk", "audit", "governance", "privacy", "gdpr", "hipaa"],
    },
    "Testing & Calidad": {
        "strong": [
            "test", "testing", "tdd", "qa", "quality", "e2e", "playwright",
            "cypress", "pytest", "jest", "regression", "coverage",
            "verification", "validate", "validation", "lint", "linter",
            "code review", "review", "benchmark", "evaluation", "eval",
            "assert", "mock", "fixture", "debug", "debugging", "bug",
        ],
        "weak": ["check", "quality gate", "gate", "audit"],
    },
    "Verticales Especializados": {
        "strong": [
            "health", "medical", "clinical", "patient", "fda", "hipaa",
            "legal", "lawyer", "attorney", "law", "contract", "litigation",
            "blockchain", "crypto", "web3", "nft", "defi", "smart contract",
            "solidity", "education", "student", "curriculum", "classroom",
            "school", "exam", "study", "teacher", "science", "scientific",
            "physics", "chemistry", "biology", "astronomy", "quantum",
            "game", "unity", "unreal", "godot", "leiloeiro", "leilao",
            "auction", "research", "literature review", "academic",
            "paper", "citation", "qms", "iso 13485", "regulatory",
            "logistics", "carrier", "shipping", "freight", "nutrition",
            "fitness", "wellness", "diagnosis", "therapy", "insurance",
            "real estate", "construction", "manufacturing",
        ],
        "weak": ["academic", "journal", "compliance"],
    },
    "Diseño & Contenido": {
        "strong": [
            "design", "ui", "ux", "figma", "graphic", "illustration",
            "typography", "color", "layout", "logo", "icon",
            "favicon", "css", "animation", "podcast",
            "voice", "image", "photo", "writing",
            "copywriting", "copy", "blog", "article", "documentation",
            "seo", "storyboard", "carousel", "presentation", "slide",
            "ppt", "pdf", "spreadsheet", "xlsx", "docx", "transcri",
            "caption", "subtitle", "aesthetic", "visual", "creative",
            "photopea", "canva", "3d model", "render", "shader",
        ],
        "weak": ["style", "theme", "template", "generator", "brand", "content",
                 "media", "video", "audio"],
    },
    "Negocio & Marketing": {
        "strong": [
            "business", "marketing", "sales", "revenue", "revops",
            "growth", "startup", "pricing", "customer", "crm",
            "advertising", "campaign", "brand strategy", "market",
            "competitor", "competitive", "finance", "financial",
            "accounting", "invoice", "billing", "consult", "ecommerce",
            "e-commerce", "shopify", "chro", "cco", "cfo", "cmo", "ceo",
            "cro advisor", "c-level", "executive", "advisor", "founder",
            "investor", "fundrais", "kpi", "metrics", "analytics",
            "roi", "conversion", "lead generation", "demand gen",
            "aso", "app store optimization", "social media",
            "influencer", "monetization", "subscription", "referral",
            "psycholog", "persuasion", "pitch", "objection",
            "loss aversion", "social proof", "subject line",
            "headline", "webinar", "partnership",
        ],
        "weak": ["strategy", "plan", "report", "review board", "cro",
                 "trust", "urgency", "scarcity"],
    },
    "Gestión de Proyectos & Equipos": {
        "strong": [
            "project management", "product management", "roadmap",
            "sprint", "scrum", "agile", "backlog", "planning",
            "collaboration", "team", "standup", "retrospective",
            "stakeholder", "okr", "jira", "linear", "asana", "trello",
            "meeting", "onboarding", "hiring", "org structure",
            "culture", "hr", "people leadership", "task coordination",
            "delivery", "milestone", "workload",
        ],
        "weak": ["coordination", "management"],
    },
    "Cloud, DevOps & Automatización": {
        "strong": [
            "cloud", "aws", "azure", "gcp", "kubernetes", "k8s", "docker",
            "container", "terraform", "devops", "cicd", "ci/cd",
            "deployment", "deploy", "infrastructure", "automation",
            "automate", "workflow", "pipeline", "observability",
            "monitoring", "incident", "reliability", "sre", "chaos",
            "capacity", "quota", "provisioning", "orchestrate infra",
            "n8n", "zapier", "integration platform", "serverless",
            "helm", "gitops", "cron", "scheduler", "runbook",
            "playbook", "on-call", "on call", "postmortem",
            "post-mortem", "post mortem",
        ],
        "weak": ["setup", "config", "environment", "sync"],
    },
    "AI & Agents": {
        "strong": [
            "agent", "agents", "ai ", " ai", "llm", "gpt",
            "prompt engineering", "prompt template", "prompt",
            "rag", "embedding", "vector", "model", "inference",
            "machine learning", "ml ", "training", "fine-tun",
            "autonomous", "orchestrator", "multi-agent", "chatbot",
            "claude", "mcp", "memory system", "context window",
            "hallucination", "reasoning", "copilot", "assistant",
        ],
        "weak": ["intelligence", "automated reasoning", "cognitive"],
    },
    "Desarrollo de Software": {
        "strong": [
            "development", "developer", "code", "coding", "software",
            "api", "backend", "frontend", "database", "sql", "query",
            "framework", "library", "architecture", "microservice",
            "python", "javascript", "typescript", "java", "golang",
            "rust", "swift", "kotlin", "react", "vue", "angular",
            "nextjs", "django", "fastapi", "mobile", "android", "ios",
            "app", "application", "compiler", "build", "package",
            "refactor", "engineering", "programming", "git", "repo",
            "sdk", "cli", "terminal", "shell", "script",
        ],
        "weak": ["tool", "system", "component", "module"],
    },
    "Meta & Productividad Personal": {
        "strong": [
            "productivity", "skill authoring", "skill creator",
            "personal", "note", "notes", "todo", "reminder",
            "knowledge management", "obsidian", "notion",
            "self-improvement", "context optimization",
            "meta skill", "claude code session", "cost tracking",
            "diary", "journal",
        ],
        "weak": ["general", "setup", "extract", "generate", "create",
                 "customize", "manage"],
    },
}


def _score_taxonomy_bucket(combined_text, token_set, rule, min_substring_len=1):
    """Shared keyword scorer for both the top-level classifier
    (infer_new_taxonomy_category, via NEW_TAXONOMY_RULES) and the
    subcategory classifier (infer_subcategory, via SUBCATEGORY_RULES).

    `min_substring_len` gates the no-word-boundary substring fallback
    (e.g. "ui" inside "guide"/"require", "orm" inside "format"/"transform").
    Defaults to 1 (fallback always allowed) to exactly preserve the
    already-validated top-level classifier behavior from task 1/2 — do not
    change that call site's default. infer_subcategory() passes a higher
    value (see call site) because a task-3 audit (2026-07-23) found this
    substring fallback produces real false positives for short keywords,
    same bug class as the "defi"/"token" false positives already fixed in
    task 2 — see topic antigravity-awesome-skills/skills-subcategory-taxonomy.
    Scoped to subcategory scoring only so it can't flip any previously
    shipped top-level category.
    """
    score = 0
    for keyword in rule.get("strong", []):
        if " " in keyword:
            if keyword in combined_text:
                score += 5
        elif keyword in token_set:
            score += 4
        elif len(keyword) >= min_substring_len and keyword in combined_text:
            score += 2
    for keyword in rule.get("weak", []):
        if " " in keyword:
            if keyword in combined_text:
                score += 2
        elif keyword in token_set:
            score += 1
    return score


def infer_new_taxonomy_category(skill_id, skill_name, description):
    """Direct classifier into one of the 10 final buckets. Always returns a
    bucket (never None) so no skill remains 'uncategorized' after generation.
    """
    normalized_name = skill_name if isinstance(skill_name, str) else ""
    normalized_description = description if isinstance(description, str) else ""
    combined_text = f"{skill_id} {normalized_name} {normalized_description}".lower()
    token_set = set(tokenize(combined_text))

    scores = {}
    for bucket, rule in NEW_TAXONOMY_RULES.items():
        score = _score_taxonomy_bucket(combined_text, token_set, rule)
        if score > 0:
            scores[bucket] = score

    if not scores:
        return "Meta & Productividad Personal"

    best_score = max(scores.values())
    candidates = [bucket for bucket, score in scores.items() if score == best_score]
    if len(candidates) > 1:
        candidates.sort(key=lambda bucket: NEW_TAXONOMY_BUCKET_PRIORITY.index(bucket))
    return candidates[0]


# --- Curated top-level-category fixes for the direct-classifier set (2026-07-23) --
# infer_new_taxonomy_category() above is a keyword classifier and, like any
# keyword classifier, gets a slice of the ~866 previously-"uncategorized"
# skills wrong (a name/description keyword pulls it toward the wrong bucket,
# e.g. "vercel-cli-with-tokens" scoring as Seguridad because of "auth"/"token").
# These ids were confirmed by manual review to sit in the wrong one of the 10
# buckets; the override wins over infer_new_taxonomy_category()'s guess.
# Originally scoped only to the direct-classifier ("is None" branch) set, but
# as of task 3 (2026-07-23) this dict is also consulted from the
# TAXONOMY_MAP-routed branch (id-keyed, so it's safe either way) — see the
# odoo-* entries below, a real TAXONOMY_MAP-level miscategorization: the
# blanket ("odoo-", "business") FAMILY_CATEGORY_RULES prefix routes every
# odoo-* skill into Negocio & Marketing even though many are pure Odoo
# module-development/API/ops skills with zero business-strategy content.
NEW_TAXONOMY_CATEGORY_OVERRIDES = {
    # The 5 seed corrections confirmed directly by repo owner review.
    "cv-tailor": "Meta & Productividad Personal",
    "creating-financial-models": "Negocio & Marketing",
    "connections-optimizer": "Negocio & Marketing",
    "bill-gates": "Negocio & Marketing",
    "TEMPLATE": "Meta & Productividad Personal",
    # Meta-skill / Claude Code tooling wrongly scored into AI & Agents,
    # Seguridad, Cloud DevOps, or Testing because of "skill"/"audit"/"token"
    # keyword collisions — these are actually skill-authoring, session, or
    # Claude Code housekeeping tools, not the domain their old bucket implies.
    "template": "Meta & Productividad Personal",
    "template-skill": "Meta & Productividad Personal",
    "handoff": "Meta & Productividad Personal",
    "skills-handoff": "Meta & Productividad Personal",
    "project-skill-audit": "Meta & Productividad Personal",
    "config-gc": "Meta & Productividad Personal",
    "extract": "Meta & Productividad Personal",
    "find-skills": "Meta & Productividad Personal",
    "promote": "Meta & Productividad Personal",
    "related-skill": "Meta & Productividad Personal",
    "skillify": "Meta & Productividad Personal",
    "write-a-skill": "Meta & Productividad Personal",
    "engineer-skill-creator": "Meta & Productividad Personal",
    "workspace-surface-audit": "Meta & Productividad Personal",
    "collab-proof": "Meta & Productividad Personal",
    "migrate-to-codex": "Meta & Productividad Personal",
    "nanoclaw-repl": "Meta & Productividad Personal",
    "skillopt-sleep": "Meta & Productividad Personal",
    "cost-tracking": "Meta & Productividad Personal",
    "writing-skills": "Meta & Productividad Personal",
    "caveman": "Meta & Productividad Personal",
    "token-budget-advisor": "Meta & Productividad Personal",
    "memory-status": "Meta & Productividad Personal",
    "engineering-team__self-improving-agent__skills__status": "Meta & Productividad Personal",
    "weekly-review": "Meta & Productividad Personal",
    "messages-ops": "Meta & Productividad Personal",
    "homelab-network-setup": "Meta & Productividad Personal",
    # legacy category "engineering-team" is a plugin/namespace folder name,
    # not a topic — TAXONOMY_MAP routed it wholesale into Cloud DevOps &
    # Automatización, which was wrong for most of its 15 heterogeneous
    # skills. Found via independent spot-check (repo owner, 2026-07-23).
    "a11y-audit": "Testing & Calidad",
    "engineering-team__code-reviewer": "Testing & Calidad",
    "email-template-builder": "Diseño & Contenido",
    "epic-design": "Diseño & Contenido",
    "self-improving-agent": "Meta & Productividad Personal",
    "senior-backend": "Desarrollo de Software",
    "senior-qa": "Testing & Calidad",
    "tdd-guide": "Testing & Calidad",
    "tech-stack-evaluator": "Desarrollo de Software",
    # Found by independent code review (2026-07-23): the legacy classifier's
    # 2-point ambiguity margin let "web-development" (score 4) edge out
    # "testing" (score 3) for this specific description; all 8 sibling
    # playwright-* skills classified correctly, only the bare "playwright"
    # id fell through.
    "playwright": "Testing & Calidad",
    # Compliance/audit tooling wrongly scored outside Seguridad.
    "soc2-compliance": "Seguridad",
    "soc2-audit-prep": "Seguridad",
    "compliance-os": "Seguridad",
    "compliance-os-bundle": "Seguridad",
    "infinity": "Seguridad",
    # Non-security tools that scored into Seguridad on "audit"/"auth"/"token".
    "tos-clause-scanner": "Verticales Especializados",
    "vercel-cli-with-tokens": "Cloud, DevOps & Automatización",
    "mailtrap-setting-up-sending-domain": "Cloud, DevOps & Automatización",
    "network-interface-health": "Cloud, DevOps & Automatización",
    "network-bgp-diagnostics": "Cloud, DevOps & Automatización",
    # Business/finance/growth tools that scored into an engineering bucket.
    "social-graph-ranker": "Negocio & Marketing",
    "crosspost": "Negocio & Marketing",
    "onboarding": "Negocio & Marketing",
    "onboarding-psychologist": "Negocio & Marketing",
    "raffle-winner-picker": "Negocio & Marketing",
    "financial-analyst": "Negocio & Marketing",
    "financial-health": "Negocio & Marketing",
    "vc-industry-research": "Negocio & Marketing",
    "xvary-stock-research": "Negocio & Marketing",
    "procurement-optimizer": "Negocio & Marketing",
    "vendor-management": "Negocio & Marketing",
    "saas-health": "Negocio & Marketing",
    "yield-intelligence": "Negocio & Marketing",
    "scenario-war-room": "Negocio & Marketing",
    "cpo-review": "Negocio & Marketing",
    "prospecting": "Negocio & Marketing",
    "churn-prevention": "Negocio & Marketing",
    "marketing-skill": "Negocio & Marketing",
    "marketing-skills": "Negocio & Marketing",
    "generating-python-installer": "Desarrollo de Software",
    "startup-cto": "Desarrollo de Software",
    # Content/SEO/design tools that scored into Gestión or Testing.
    "seo-schema": "Diseño & Contenido",
    "explainer-video-guide": "Diseño & Contenido",
    "youtube-thumbnail-design": "Diseño & Contenido",
    "schema": "Diseño & Contenido",
    "seo-page": "Diseño & Contenido",
    "seo-programmatic": "Diseño & Contenido",
    "seo-hreflang": "Diseño & Contenido",
    "internal-comms": "Diseño & Contenido",
    "motion-advanced": "Diseño & Contenido",
    "motion-foundations": "Diseño & Contenido",
    "motion-patterns": "Diseño & Contenido",
    "make-interfaces-feel-better": "Diseño & Contenido",
    "interface-design": "Diseño & Contenido",
    # Dev-pattern skills that scored outside Desarrollo de Software (mostly
    # untranslated-stub descriptions with only the id as signal).
    "matematico-tao": "Desarrollo de Software",
    "r3f-animation": "Desarrollo de Software",
    "laravel-plugin-discovery": "Desarrollo de Software",
    "jpa-patterns": "Desarrollo de Software",
    "kql": "Desarrollo de Software",
    "compose-multiplatform-patterns": "Desarrollo de Software",
    "swift-actor-persistence": "Desarrollo de Software",
    "content-hash-cache-pattern": "Desarrollo de Software",
    "invariant-guard": "Desarrollo de Software",
    "lemmaly": "Desarrollo de Software",
    "bun-runtime": "Desarrollo de Software",
    "ck": "Desarrollo de Software",
    "redis-patterns": "Desarrollo de Software",
    "quarkus-patterns": "Desarrollo de Software",
    "new-rails-project": "Desarrollo de Software",
    "complexity-cuts": "Testing & Calidad",
    "quinn": "Testing & Calidad",
    "pagespeed-enhancer": "Testing & Calidad",
    "risk-management-specialist": "Verticales Especializados",
    "project-health": "Gestión de Proyectos & Equipos",
    "culture-architect": "Gestión de Proyectos & Equipos",
    "gan-style-harness": "AI & Agents",
    # odoo-* TAXONOMY_MAP-level correction (task 3, 2026-07-23): the
    # ("odoo-", "business") FAMILY_CATEGORY_RULES prefix match routes every
    # odoo-* skill to Negocio & Marketing, but these specific ids are pure
    # module-development/API/ORM/testing/ops content — no business-strategy
    # signal at all. Business/functional-consultant odoo-* skills (accounting
    # setup, HR payroll, sales/CRM, manufacturing advisor, etc.) are left
    # alone; only the unambiguous developer-facing ones move.
    "odoo-module-developer": "Desarrollo de Software",
    "odoo-orm-expert": "Desarrollo de Software",
    "odoo-xml-views-builder": "Desarrollo de Software",
    "odoo-rpc-api": "Desarrollo de Software",
    "odoo-security-rules": "Desarrollo de Software",
    "odoo-qweb-templates": "Desarrollo de Software",
    "odoo-automated-tests": "Desarrollo de Software",
    "odoo-performance-tuner": "Desarrollo de Software",
    "odoo-migration-helper": "Desarrollo de Software",
    "odoo-shopify-integration": "Desarrollo de Software",
    "odoo-woocommerce-bridge": "Desarrollo de Software",
    "odoo-backup-strategy": "Cloud, DevOps & Automatización",
    "odoo-docker-deployment": "Cloud, DevOps & Automatización",
}


# --- Subcategory taxonomy for the direct-classifier set (2026-07-23) --------
# Second classification level. Originally scoped only to skills whose
# top-level category was resolved by infer_new_taxonomy_category() above (the
# ~866 skills that had no legacy category at all). As of task 3
# (2026-07-23), TAXONOMY_MAP-routed skills (the other ~2003) get a
# subcategory pass too — see LEGACY_CATEGORY_SUBCATEGORY_MAP and the
# `legacy_category` parameter on infer_subcategory() below. Confirmed list,
# do not invent values outside it; "General" is the explicit catch-all for
# genuine non-fits.
SUBCATEGORY_TAXONOMY = {
    "AI & Agents": ["Modelos & RAG", "Agentes Multi-Agente", "MCP & Herramientas", "MLOps & Datos"],
    "Desarrollo de Software": [
        "Backend", "Frontend & Web", "Mobile", "Lenguajes & Frameworks",
        "Arquitectura & Patrones", "APIs & Integraciones", "Bases de Datos",
    ],
    "Cloud, DevOps & Automatización": [
        "Cloud Providers", "CI/CD & Deployment", "Contenedores & Orquestación",
        "Automatización (Zapier/n8n/Rube)", "Observability & Reliability",
    ],
    "Seguridad": ["Pentesting & Red Team", "Auditoría & Compliance", "AppSec", "Seguridad Cloud/Infra"],
    "Testing & Calidad": [
        "Testing Automatizado", "Code Review & Calidad", "Performance & Benchmarking", "Accesibilidad (a11y)",
    ],
    "Diseño & Contenido": [
        "UI/UX & Diseño de Producto", "Generación de Contenido",
        "Branding & Identidad Visual", "Documentación & Redacción Técnica",
    ],
    "Negocio & Marketing": [
        "Marketing & Growth", "Finanzas & Analítica", "Advisory Ejecutivo (C-level)", "Ventas & Customer Success",
    ],
    "Gestión de Proyectos & Equipos": [
        "Agile/Scrum & Backlog", "Herramientas (Jira/Atlassian)", "Liderazgo & Cambio Organizacional",
    ],
    "Verticales Especializados": [
        "Legal & Regulatorio", "Salud & Ciencias", "Finanzas/Blockchain", "Educación & Investigación", "Gaming",
    ],
    "Meta & Productividad Personal": [
        "Meta-skills (sobre Claude/Agentes)", "Productividad Personal",
        "Homelab & Infra Personal", "Aprendizaje Continuo",
    ],
}

SUBCATEGORY_RULES = {
    "AI & Agents": {
        "priority": ["Modelos & RAG", "MLOps & Datos", "MCP & Herramientas", "Agentes Multi-Agente"],
        "rules": {
            "Modelos & RAG": {
                "strong": [
                    "rag", "embedding", "vector search", "llm", "gpt", "claude api", "gemini",
                    "prompt engineering", "prompt template", "fine-tun", "chatbot", "flux",
                    "image generation", "text-to-speech", "speech-to-text", "multimodal",
                    "computer vision", "voice clone", "video generation", "text-to-image",
                    "inference api",
                ],
                "weak": ["model", "generation", "hallucination", "reasoning"],
            },
            "MLOps & Datos": {
                "strong": [
                    "ml pipeline", "machine learning", "mlops", "ml ops", "dataset", "training data",
                    "data pipeline", "vector store", "knowledge base", "knowledge management",
                    "memory system", "cost tracking", "context window", "context restore",
                    "context save", "token cost", "token usage", "context optimization",
                    "compaction",
                ],
                "weak": ["data", "pipeline"],
            },
            "MCP & Herramientas": {
                "strong": [
                    "mcp server", "mcp tool", "mcp", "tool design", "tool calling",
                    "tool consolidation", "governance", "protocol",
                ],
                "weak": ["tool", "api", "connector", "registry"],
            },
            "Agentes Multi-Agente": {
                "strong": [
                    "multi-agent", "multi agent", "orchestrator", "orchestrate", "subagent",
                    "parallel agent", "agent team", "worktree", "swarm", "autonomous agent",
                    "harness", "board meeting", "spawn", "dag", "team composition",
                ],
                "weak": ["agent", "agents", "loop", "autonomous"],
            },
        },
    },
    "Desarrollo de Software": {
        "priority": [
            "Bases de Datos", "Mobile", "Frontend & Web", "Backend",
            "Lenguajes & Frameworks", "APIs & Integraciones", "Arquitectura & Patrones",
        ],
        "rules": {
            "Bases de Datos": {
                "strong": [
                    "database", "sql", "postgres", "postgresql", "mysql", "redis", "mongodb", "orm",
                    "query optimization", "schema design", "jpa", "hibernate", "kql", "clickhouse",
                    "nosql", "sqlite",
                ],
                "weak": ["query", "migration", "index"],
            },
            "Mobile": {
                "strong": [
                    "mobile", "ios", "android", "swift", "swiftui", "kotlin", "flutter",
                    "react native", "xcode", "jetpack compose", "compose multiplatform", "app store",
                ],
                "weak": [],
            },
            "Frontend & Web": {
                "strong": [
                    "frontend", "react", "vue", "angular", "nextjs", "next.js", "svelte", "css",
                    "html", "web app", "browser", "dom", "three.js", "r3f", "webgl", "vite",
                    "tailwind", "web component", "electron", "desktop app",
                ],
                "weak": ["ui component", "web"],
            },
            "Backend": {
                "strong": [
                    "backend", "microservice", "server-side", "django", "fastapi", "spring boot",
                    "express", "nestjs", "node.js", "endpoint", "caching", "cache",
                    "background job", "queue",
                ],
                "weak": ["server", "service"],
            },
            "Lenguajes & Frameworks": {
                "strong": [
                    "python", "javascript", "typescript", "java ", "golang", "rust", "c++", "c#",
                    ".net", "dotnet", "ruby", "php", "elixir", "scala", "perl", "dart", "bash",
                    "shell script", "posix", "bun", "deno", "quarkus", "rails", "laravel",
                    "language-specific", "coding guidelines", "idiomatic",
                ],
                "weak": ["framework", "language", "runtime"],
            },
            "APIs & Integraciones": {
                "strong": [
                    "api integration", "webhook", "sdk", "graphql schema", "rest api",
                    "third-party integration", "oauth integration", "cli tool", "package manager",
                ],
                "weak": ["integration", "sdk"],
            },
            "Arquitectura & Patrones": {
                "strong": [
                    "architecture", "design pattern", "refactor", "clean code", "solid",
                    "domain-driven", "hexagonal", "monorepo", "system design", "algorithm",
                    "big-o", "complexity", "code review", "technical debt", "code quality",
                    "debugging", "debug", "bug", "error handling", "error analysis",
                    "stack trace", "root cause", "diagnose", "diagnosing",
                ],
                "weak": ["pattern", "design", "structure"],
            },
        },
    },
    "Cloud, DevOps & Automatización": {
        "priority": [
            "Contenedores & Orquestación", "CI/CD & Deployment", "Observability & Reliability",
            "Automatización (Zapier/n8n/Rube)", "Cloud Providers",
        ],
        "rules": {
            "Contenedores & Orquestación": {
                "strong": ["docker", "kubernetes", "k8s", "helm", "container", "orchestration", "service mesh"],
                "weak": [],
            },
            "CI/CD & Deployment": {
                "strong": [
                    "ci/cd", "cicd", "deploy", "deployment", "pipeline", "github actions",
                    "gitlab ci", "release", "changelog", "netlify", "vercel", "cloudflare", "render",
                    "pull request", "git workflow", "conventional commit",
                ],
                "weak": ["build", "publish", "git", "github", "commit", "branch", "merge", "worktree"],
            },
            "Observability & Reliability": {
                "strong": [
                    "observability", "monitoring", "incident", "reliability", "sre",
                    "chaos engineering", "postmortem", "runbook", "on-call", "alert", "canary",
                    "network diagnostics", "network interface", "bgp",
                ],
                "weak": ["health", "diagnostic"],
            },
            "Automatización (Zapier/n8n/Rube)": {
                "strong": [
                    "zapier", "n8n", "rube", "composio", "automate", "automation",
                    "workflow automation", "webhook automation", "mailtrap", "supabase automation",
                ],
                "weak": ["automate", "sync"],
            },
            "Cloud Providers": {
                "strong": [
                    "aws", "azure", "gcp", "google cloud", "cloud cost", "cost optimization",
                    "capacity", "quota", "region",
                ],
                "weak": ["cloud"],
            },
        },
    },
    "Seguridad": {
        "priority": ["Pentesting & Red Team", "Auditoría & Compliance", "AppSec", "Seguridad Cloud/Infra"],
        "rules": {
            "Pentesting & Red Team": {
                "strong": [
                    "red team", "pentest", "penetration", "exploit", "threat hunt",
                    "threat detection", "reconnaissance", "attack path", "mitre att&ck",
                    "vulnerability scan", "reverse engineering", "disassembly",
                    "decompilation", "binary analysis", "memory forensics",
                    "malware analysis", "protocol reverse engineering", "wireshark",
                    "packet analysis", "obfuscation", "anti-reversing",
                ],
                "weak": ["attack", "threat"],
            },
            "Auditoría & Compliance": {
                "strong": [
                    "audit", "compliance", "iso 27001", "iso27001", "soc 2", "soc2", "gdpr",
                    "hipaa", "governance", "risk assessment", "supply chain risk",
                    "privacy by design", "ciso", "ownership map", "bus factor",
                ],
                "weak": ["risk", "policy"],
            },
            "AppSec": {
                "strong": [
                    "appsec", "authn", "authz", "authentication", "authorization", "csrf", "xss",
                    "sqli", "injection", "input validation", "code security", "secure code",
                    "sast", "semgrep", "dependency vulnerability", "sbom", "file upload",
                    "side-channel", "timing attack", "constant-time",
                    "static application security testing",
                ],
                "weak": ["auth", "security review"],
            },
            "Seguridad Cloud/Infra": {
                "strong": [
                    "secrets manager", "secrets management", "container security", "hardening",
                    "zero trust", "service mesh security", "infra security", "mtls", "linkerd",
                    "service mesh",
                ],
                "weak": ["secrets", "infra"],
            },
        },
    },
    "Testing & Calidad": {
        "priority": [
            "Accesibilidad (a11y)", "Performance & Benchmarking", "Testing Automatizado", "Code Review & Calidad",
        ],
        "rules": {
            "Accesibilidad (a11y)": {
                "strong": ["accessibility", "a11y", "wcag", "screen reader", "aria"],
                "weak": [],
            },
            "Performance & Benchmarking": {
                "strong": [
                    "performance", "benchmark", "latency", "throughput", "optimization",
                    "profiling", "load test", "page speed", "lighthouse", "big-o", "complexity",
                ],
                "weak": ["speed", "optimize"],
            },
            "Testing Automatizado": {
                "strong": [
                    "test", "testing", "tdd", "e2e", "playwright", "cypress", "pytest", "jest",
                    "unit test", "integration test", "test suite", "coverage", "verification",
                    "debug", "debugging",
                ],
                "weak": ["qa", "quality"],
            },
            "Code Review & Calidad": {
                "strong": ["code review", "review", "lint", "linter", "static analysis", "code quality", "refactor"],
                "weak": ["quality"],
            },
        },
    },
    "Diseño & Contenido": {
        "priority": [
            "Branding & Identidad Visual", "Documentación & Redacción Técnica",
            "UI/UX & Diseño de Producto", "Generación de Contenido",
        ],
        "rules": {
            "Branding & Identidad Visual": {
                "strong": ["brand", "branding", "logo", "identity", "brand guideline", "brand voice", "visual identity"],
                "weak": [],
            },
            "Documentación & Redacción Técnica": {
                "strong": [
                    "documentation", "technical writing", "readme", "adr", "tutorial", "changelog",
                    "writing guideline", "internal comms", "internal communication",
                    "proofreading", "editing",
                ],
                "weak": ["docs", "writing"],
            },
            "UI/UX & Diseño de Producto": {
                "strong": [
                    "ui", "ux", "design system", "figma", "interface design", "interaction design",
                    "wireframe", "prototype", "usability", "persona", "user research",
                    "accessibility-first design", "motion design", "animation guide",
                    "web app implementation guide",
                ],
                "weak": ["interface", "layout", "design"],
            },
            "Generación de Contenido": {
                "strong": [
                    "content", "article", "blog", "copywriting", "video production",
                    "image generation", "podcast", "infographic", "presentation", "slide deck",
                    "seo", "social media", "carousel", "thumbnail", "illustration", "transcript",
                    "translate", "voiceover",
                ],
                "weak": ["generate", "create"],
            },
        },
    },
    "Negocio & Marketing": {
        "priority": [
            "Advisory Ejecutivo (C-level)", "Finanzas & Analítica", "Ventas & Customer Success", "Marketing & Growth",
        ],
        "rules": {
            "Advisory Ejecutivo (C-level)": {
                "strong": [
                    "ceo", "cfo", "cmo", "cro advisor", "coo", "cpo", "cto advisor", "ciso", "chro",
                    "c-level", "c-suite", "board meeting", "executive", "founder mode", "investor",
                    "board deck", "chief of staff",
                ],
                "weak": ["advisor", "leadership"],
            },
            "Finanzas & Analítica": {
                "strong": [
                    "financial", "finance", "dcf", "valuation", "budget", "revenue", "arr", "mrr",
                    "churn rate", "saas metrics", "invoice", "accounting", "billing", "stock",
                    "equity", "investment", "kpi", "analytics", "metrics",
                ],
                "weak": ["money", "cost"],
            },
            "Ventas & Customer Success": {
                "strong": [
                    "sales", "customer success", "crm", "prospecting", "cold email", "outreach",
                    "customer retention", "vendor management", "procurement", "rfp", "onboarding",
                    "activation", "lead generation",
                ],
                "weak": ["customer", "client"],
            },
            "Marketing & Growth": {
                "strong": [
                    "marketing", "growth", "campaign", "advertising", "seo", "aso", "social media",
                    "brand awareness", "content marketing", "email marketing", "referral", "pricing",
                    "conversion", "cro", "landing page", "webinar", "newsletter", "pr",
                    "public relations", "psycholog", "headline", "subject line", "competitive matrix",
                    "positioning",
                ],
                "weak": ["audience", "channel"],
            },
        },
    },
    "Gestión de Proyectos & Equipos": {
        "priority": ["Herramientas (Jira/Atlassian)", "Agile/Scrum & Backlog", "Liderazgo & Cambio Organizacional"],
        "rules": {
            "Herramientas (Jira/Atlassian)": {
                "strong": [
                    "jira", "atlassian", "confluence", "trello", "linear", "asana", "notion",
                    "basecamp", "freshservice", "monday.com", "miro", "todoist", "wrike", "itsm",
                ],
                "weak": [],
            },
            "Agile/Scrum & Backlog": {
                "strong": [
                    "agile", "scrum", "sprint", "backlog", "user story", "retrospective", "standup",
                    "roadmap", "okr", "rice", "kanban", "capacity planning", "project sizing",
                    "feature flag", "issue tracker", "prd", "project manager",
                ],
                "weak": ["planning", "estimate"],
            },
            "Liderazgo & Cambio Organizacional": {
                "strong": [
                    "culture", "change management", "hiring", "org structure", "leadership",
                    "team composition", "onboarding process", "org chart", "hr", "people leadership",
                ],
                "weak": ["team", "org"],
            },
        },
    },
    "Verticales Especializados": {
        "priority": ["Salud & Ciencias", "Legal & Regulatorio", "Finanzas/Blockchain", "Gaming", "Educación & Investigación"],
        "rules": {
            "Salud & Ciencias": {
                "strong": [
                    "health", "medical", "clinical", "patient", "fda", "hipaa", "hospital",
                    "risk management", "iso 13485", "iso 14971", "qms", "science", "scientific",
                    "biology", "physics", "chemistry", "astronomy", "genome", "pubmed",
                ],
                "weak": [],
            },
            "Legal & Regulatorio": {
                "strong": [
                    "legal", "lawyer", "attorney", "contract review", "regulatory", "gdpr",
                    "terms of service", "privacy policy", "compliance checklist", "litigation",
                    "patent", "trademark", "uspto",
                ],
                "weak": ["law", "regulation"],
            },
            "Finanzas/Blockchain": {
                "strong": [
                    "blockchain", "crypto", "web3", "nft", "smart contract", "solidity", "evm",
                    "reentrancy", "amm", "liquidity pool",
                ],
                "weak": [],
            },
            "Gaming": {
                "strong": [
                    "game design", "game development", "unity", "unreal", "godot",
                    "multiplayer game", "game art", "game audio",
                ],
                "weak": ["game"],
            },
            "Educación & Investigación": {
                "strong": [
                    "research", "academic", "literature review", "citation", "paper", "curriculum",
                    "student", "education", "exam", "study", "grant",
                ],
                "weak": ["learn", "teach"],
            },
        },
    },
    "Meta & Productividad Personal": {
        "priority": [
            "Homelab & Infra Personal", "Meta-skills (sobre Claude/Agentes)", "Aprendizaje Continuo", "Productividad Personal",
        ],
        "rules": {
            "Homelab & Infra Personal": {
                "strong": [
                    "homelab", "home lab", "pihole", "wireguard", "vlan segmentation",
                    "self-hosted", "home network",
                ],
                "weak": [],
            },
            "Meta-skills (sobre Claude/Agentes)": {
                "strong": [
                    "claude code", "skill authoring", "skill creator", "create a skill", "new skill",
                    "write a skill", "skill.md", "handoff document", "session handoff",
                    "token usage", "auto-memory", "memory consolidation", "sdd", "skill registry",
                    "meta-skill", "plugin creator", "agent configuration",
                ],
                "weak": ["skill", "session"],
            },
            "Aprendizaje Continuo": {
                "strong": [
                    "continuous learning", "learning resource", "growth log", "developer growth",
                    "self-improvement",
                ],
                "weak": ["learn"],
            },
            "Productividad Personal": {
                "strong": [
                    "productivity", "note", "notes", "todo", "reminder", "journal", "diary",
                    "obsidian", "deep work", "weekly review", "gtd", "inbox", "personal knowledge",
                    "speed reading",
                ],
                "weak": ["personal", "organize"],
            },
        },
    },
}

# Curated per-id subcategory pins — covers (a) the 5 category-correction
# examples given alongside this taxonomy, and (b) every id in
# NEW_TAXONOMY_CATEGORY_OVERRIDES above (its corrected category may not have
# obvious keyword signal for the right subcategory, so pin it explicitly
# rather than trust the keyword scorer against a category the description
# wasn't written for).
SUBCATEGORY_OVERRIDES = {
    "cv-tailor": "Productividad Personal",
    "creating-financial-models": "Finanzas & Analítica",
    "connections-optimizer": "Marketing & Growth",
    "bill-gates": "Advisory Ejecutivo (C-level)",
    "TEMPLATE": "Meta-skills (sobre Claude/Agentes)",
    "template": "Meta-skills (sobre Claude/Agentes)",
    "template-skill": "Meta-skills (sobre Claude/Agentes)",
    "handoff": "Meta-skills (sobre Claude/Agentes)",
    "skills-handoff": "Meta-skills (sobre Claude/Agentes)",
    "project-skill-audit": "Meta-skills (sobre Claude/Agentes)",
    "config-gc": "Meta-skills (sobre Claude/Agentes)",
    "extract": "Meta-skills (sobre Claude/Agentes)",
    "find-skills": "Meta-skills (sobre Claude/Agentes)",
    "promote": "Meta-skills (sobre Claude/Agentes)",
    "related-skill": "Meta-skills (sobre Claude/Agentes)",
    "skillify": "Meta-skills (sobre Claude/Agentes)",
    "write-a-skill": "Meta-skills (sobre Claude/Agentes)",
    "engineer-skill-creator": "Meta-skills (sobre Claude/Agentes)",
    "workspace-surface-audit": "Meta-skills (sobre Claude/Agentes)",
    "collab-proof": "Meta-skills (sobre Claude/Agentes)",
    "migrate-to-codex": "Meta-skills (sobre Claude/Agentes)",
    "nanoclaw-repl": "Meta-skills (sobre Claude/Agentes)",
    "skillopt-sleep": "Meta-skills (sobre Claude/Agentes)",
    "cost-tracking": "Meta-skills (sobre Claude/Agentes)",
    "writing-skills": "Meta-skills (sobre Claude/Agentes)",
    "caveman": "Meta-skills (sobre Claude/Agentes)",
    "token-budget-advisor": "Meta-skills (sobre Claude/Agentes)",
    "memory-status": "Meta-skills (sobre Claude/Agentes)",
    "engineering-team__self-improving-agent__skills__status": "Meta-skills (sobre Claude/Agentes)",
    "weekly-review": "Productividad Personal",
    "messages-ops": "Productividad Personal",
    "homelab-network-setup": "Homelab & Infra Personal",
    # legacy "engineering-team" namespace fix, paired with
    # NEW_TAXONOMY_CATEGORY_OVERRIDES above.
    "a11y-audit": "Accesibilidad (a11y)",
    "engineering-team__code-reviewer": "Code Review & Calidad",
    "email-template-builder": "Generación de Contenido",
    "epic-design": "UI/UX & Diseño de Producto",
    "self-improving-agent": "Meta-skills (sobre Claude/Agentes)",
    "senior-backend": "Backend",
    "senior-qa": "Testing Automatizado",
    "tdd-guide": "Testing Automatizado",
    "tech-stack-evaluator": "Arquitectura & Patrones",
    "playwright": "Testing Automatizado",
    "network-bgp-diagnostics": "Observability & Reliability",
    "tos-clause-scanner": "Legal & Regulatorio",
    "vercel-cli-with-tokens": "CI/CD & Deployment",
    "mailtrap-setting-up-sending-domain": "Automatización (Zapier/n8n/Rube)",
    "network-interface-health": "Observability & Reliability",
    "soc2-compliance": "Auditoría & Compliance",
    "soc2-audit-prep": "Auditoría & Compliance",
    "compliance-os": "Auditoría & Compliance",
    "compliance-os-bundle": "Auditoría & Compliance",
    "infinity": "AppSec",
    "social-graph-ranker": "Marketing & Growth",
    "crosspost": "Marketing & Growth",
    "onboarding": "Marketing & Growth",
    "onboarding-psychologist": "Marketing & Growth",
    "raffle-winner-picker": "Marketing & Growth",
    "financial-analyst": "Finanzas & Analítica",
    "financial-health": "Finanzas & Analítica",
    "vc-industry-research": "Finanzas & Analítica",
    "xvary-stock-research": "Finanzas & Analítica",
    "procurement-optimizer": "Finanzas & Analítica",
    "vendor-management": "Finanzas & Analítica",
    "saas-health": "Finanzas & Analítica",
    "yield-intelligence": "Finanzas & Analítica",
    "scenario-war-room": "Advisory Ejecutivo (C-level)",
    "cpo-review": "Advisory Ejecutivo (C-level)",
    "prospecting": "Ventas & Customer Success",
    "churn-prevention": "Ventas & Customer Success",
    "marketing-skill": "Marketing & Growth",
    "marketing-skills": "Marketing & Growth",
    "seo-schema": "Generación de Contenido",
    "explainer-video-guide": "Generación de Contenido",
    "youtube-thumbnail-design": "Generación de Contenido",
    "schema": "Generación de Contenido",
    "seo-page": "Generación de Contenido",
    "seo-programmatic": "Generación de Contenido",
    "seo-hreflang": "Generación de Contenido",
    "internal-comms": "Documentación & Redacción Técnica",
    "motion-advanced": "UI/UX & Diseño de Producto",
    "motion-foundations": "UI/UX & Diseño de Producto",
    "motion-patterns": "UI/UX & Diseño de Producto",
    "make-interfaces-feel-better": "UI/UX & Diseño de Producto",
    "interface-design": "UI/UX & Diseño de Producto",
    "matematico-tao": "Arquitectura & Patrones",
    "r3f-animation": "Frontend & Web",
    "laravel-plugin-discovery": "Backend",
    "culture-architect": "Liderazgo & Cambio Organizacional",
    "generating-python-installer": "Lenguajes & Frameworks",
    "startup-cto": "Arquitectura & Patrones",
    "jpa-patterns": "Bases de Datos",
    "kql": "Bases de Datos",
    "compose-multiplatform-patterns": "Mobile",
    "swift-actor-persistence": "Mobile",
    "content-hash-cache-pattern": "Backend",
    "invariant-guard": "Arquitectura & Patrones",
    "lemmaly": "Arquitectura & Patrones",
    "bun-runtime": "Lenguajes & Frameworks",
    "ck": "Frontend & Web",
    "redis-patterns": "Bases de Datos",
    "quarkus-patterns": "Lenguajes & Frameworks",
    "new-rails-project": "Lenguajes & Frameworks",
    "complexity-cuts": "Performance & Benchmarking",
    "quinn": "Testing Automatizado",
    "pagespeed-enhancer": "Performance & Benchmarking",
    "risk-management-specialist": "Salud & Ciencias",
    "project-health": "Herramientas (Jira/Atlassian)",
    "gan-style-harness": "Agentes Multi-Agente",
    # "ios" token collision: Cisco IOS (router/switch OS) tokenizes the same
    # as Apple iOS, wrongly scoring Mobile. None of Desarrollo de Software's
    # real subcats fit network-device configuration — honest General.
    "cisco-ios-patterns": "General",
}

# --- Direct legacy-category -> subcategory signal (2026-07-23, task 3) ------
# For the ~2003 skills that went through TAXONOMY_MAP (i.e. they HAD one of
# the ~97 legacy fine-grained categories before task 1 collapsed it into one
# of the 10 buckets), that original legacy value is often a strong, cheap
# signal for the *subcategory* too — e.g. legacy "backend" -> "Backend",
# legacy "mcp" -> "MCP & Herramientas". Only legacy categories with an
# unambiguous 1:1 subcategory fit are listed here; broad/overloaded legacy
# categories (e.g. "development", "testing", "security", "design", "quality",
# "workflow", "devops", "business", "project-management") are deliberately
# left out so they fall through to the keyword scorer (SUBCATEGORY_RULES)
# below, which looks at the actual name+description instead of a coarse
# legacy label. Values must exist in SUBCATEGORY_TAXONOMY[<mapped category>]
# for the corresponding TAXONOMY_MAP target, or be the literal "General"
# catch-all (see legacy "general" below) — enforced by infer_subcategory().
LEGACY_CATEGORY_SUBCATEGORY_MAP = {
    # AI & Agents
    "ai-agents": "Agentes Multi-Agente",
    "data-ai": "MLOps & Datos",
    "data-science": "MLOps & Datos",
    "prompt-engineering": "Modelos & RAG",
    "ml-ops": "MLOps & Datos",
    "mcp": "MCP & Herramientas",
    "memory": "MLOps & Datos",
    "agent-behavior": "Agentes Multi-Agente",
    "agent-orchestration": "Agentes Multi-Agente",
    "orchestration": "Agentes Multi-Agente",
    # Desarrollo de Software
    "backend": "Backend",
    "frontend": "Frontend & Web",
    "front-end": "Frontend & Web",
    "web-development": "Frontend & Web",
    "mobile": "Mobile",
    "framework": "Lenguajes & Frameworks",
    "api-integration": "APIs & Integraciones",
    "architecture": "Arquitectura & Patrones",
    "database": "Bases de Datos",
    "database-processing": "Bases de Datos",
    # Cloud, DevOps & Automatización
    "cloud": "Cloud Providers",
    "automation": "Automatización (Zapier/n8n/Rube)",
    "reliability": "Observability & Reliability",
    "browser-automation": "Automatización (Zapier/n8n/Rube)",
    # Testing & Calidad
    "test-automation": "Testing Automatizado",
    "code-quality": "Code Review & Calidad",
    "engineering / code quality": "Code Review & Calidad",
    "ai-testing": "Testing Automatizado",
    # Diseño & Contenido
    "content": "Generación de Contenido",
    "media": "Generación de Contenido",
    "graphics-processing": "Generación de Contenido",
    "voice-agents": "Generación de Contenido",
    "document-processing": "Documentación & Redacción Técnica",
    "presentation-processing": "Generación de Contenido",
    "media-processing": "Generación de Contenido",
    "video": "Generación de Contenido",
    "seo": "Generación de Contenido",
    "documentacion-de-codigo": "Documentación & Redacción Técnica",
    # Negocio & Marketing
    "marketing": "Marketing & Growth",
    "marketing-skill": "Marketing & Growth",
    "business-growth": "Marketing & Growth",
    "growth": "Marketing & Growth",
    "consulting": "Advisory Ejecutivo (C-level)",
    "finance": "Finanzas & Analítica",
    "c-level-advisor": "Advisory Ejecutivo (C-level)",
    # Gestión de Proyectos & Equipos
    "planning": "Agile/Scrum & Backlog",
    # Verticales Especializados
    "health": "Salud & Ciencias",
    "legal": "Legal & Regulatorio",
    "blockchain": "Finanzas/Blockchain",
    "education": "Educación & Investigación",
    "science": "Salud & Ciencias",
    "game-development": "Gaming",
    "research": "Educación & Investigación",
    # Meta & Productividad Personal
    "meta": "Meta-skills (sobre Claude/Agentes)",
    "productivity": "Productividad Personal",
    "skill-authoring": "Meta-skills (sobre Claude/Agentes)",
    "context-optimization": "Meta-skills (sobre Claude/Agentes)",
    "general": "General",
    "claude.ai": "Meta-skills (sobre Claude/Agentes)",
    "antigravity-awesome-skills": "Meta-skills (sobre Claude/Agentes)",
    "knowledge-management": "Productividad Personal",
    "personal-development": "Productividad Personal",
}


def infer_subcategory(category, skill_id, skill_name, description, legacy_category=None):
    """Second-level classifier. Returns a subcategory string from
    SUBCATEGORY_TAXONOMY[category], or "General" as the explicit catch-all
    when nothing scores. Never returns None for a known category.

    Resolution order: (1) per-id pin in SUBCATEGORY_OVERRIDES, (2) direct
    legacy-category signal via LEGACY_CATEGORY_SUBCATEGORY_MAP (only for
    skills that came through TAXONOMY_MAP — pass their pre-translation
    legacy category as `legacy_category`), (3) keyword scorer below.
    """
    if skill_id in SUBCATEGORY_OVERRIDES:
        return SUBCATEGORY_OVERRIDES[skill_id]

    if legacy_category:
        mapped = LEGACY_CATEGORY_SUBCATEGORY_MAP.get(legacy_category)
        if mapped == "General" or mapped in SUBCATEGORY_TAXONOMY.get(category, []):
            return mapped

    spec = SUBCATEGORY_RULES.get(category)
    if not spec:
        return None

    normalized_name = skill_name if isinstance(skill_name, str) else ""
    normalized_description = description if isinstance(description, str) else ""
    combined_text = f"{skill_id} {normalized_name} {normalized_description}".lower()
    token_set = set(tokenize(combined_text))

    scores = {}
    for subcat, rule in spec["rules"].items():
        # min_substring_len=4: see _score_taxonomy_bucket docstring — avoids
        # short-keyword substring collisions (e.g. "orm" in "format", "ui"
        # in "guide") without touching the top-level classifier's behavior.
        score = _score_taxonomy_bucket(combined_text, token_set, rule, min_substring_len=4)
        if score > 0:
            scores[subcat] = score

    if not scores:
        return "General"

    best_score = max(scores.values())
    candidates = [subcat for subcat, score in scores.items() if score == best_score]
    if len(candidates) > 1:
        candidates.sort(key=lambda subcat: spec["priority"].index(subcat))
    return candidates[0]


def tokenize(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def infer_category(skill_id, skill_name, description):
    for prefix, category in FAMILY_CATEGORY_RULES:
        if skill_id.startswith(prefix):
            return category

    normalized_name = skill_name if isinstance(skill_name, str) else ""
    normalized_description = description if isinstance(description, str) else ""
    combined_text = f"{skill_id} {normalized_name} {normalized_description}".lower()
    token_set = set(tokenize(combined_text))
    scores = {}

    for rule in CATEGORY_RULES:
        score = 0
        strong_keywords = {keyword.lower() for keyword in rule.get("strong_keywords", [])}
        for keyword in rule["keywords"]:
            keyword_lower = keyword.lower()
            if " " in keyword_lower:
                if keyword_lower in combined_text:
                    score += 4 if keyword_lower in strong_keywords else 3
                continue

            if keyword_lower in token_set:
                score += 3 if keyword_lower in strong_keywords else 2
            elif keyword_lower in combined_text:
                score += 1

        if score > 0:
            scores[rule["name"]] = score

    if not scores:
        return None

    ranked = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    best_category, best_score = ranked[0]
    second_score = ranked[1][1] if len(ranked) > 1 else 0

    if best_score < 4:
        return None

    if best_score < 8 and (best_score - second_score) < 2:
        return None

    return best_category


def normalize_category(category):
    if not isinstance(category, str):
        return category
    return category.strip().lower()

def normalize_yaml_value(value):
    if isinstance(value, Mapping):
        return {key: normalize_yaml_value(val) for key, val in value.items()}
    if isinstance(value, list):
        return [normalize_yaml_value(item) for item in value]
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, (bytes, bytearray)):
        return bytes(value).decode("utf-8", errors="replace")
    return value


def coerce_metadata_text(value):
    if value is None or isinstance(value, (Mapping, list, tuple, set)):
        return None
    if isinstance(value, str):
        return value
    return str(value)

def coerce_metadata_tags(value):
    """Normalize a frontmatter `tags:` value into a clean list of strings.

    Ported from the pre-refactor tags parsing in tools/lib/skill-utils.js
    (readSkill), which build-catalog.js relied on before it was switched to
    read data/skills_index.json instead of scanning skills/ itself — that
    switch silently dropped curated tags for ~352 skills because
    generate_index.py never parsed `tags:` at all (found via independent
    code review, 2026-07-23). Accepts a real YAML list (`tags: [a, b]`) or a
    comma/whitespace-separated string.
    """
    if isinstance(value, (list, tuple, set)):
        return [str(tag).strip() for tag in value if str(tag).strip()]
    if isinstance(value, str) and value.strip():
        parts = re.split(r'[,\s]+', value.strip())
        return [part.strip() for part in parts if part.strip()]
    return []

def parse_frontmatter(content):
    """
    Parses YAML frontmatter, sanitizing unquoted values containing @.
    Handles single values and comma-separated lists by quoting the entire line.
    """
    fm_match = re.search(r'^---\s*\n(.*?)\n?---(?:\s*\n|$)', content, re.DOTALL)
    if not fm_match:
        return {}
    
    yaml_text = fm_match.group(1)
    
    # Process line by line to handle values containing @ and commas
    sanitized_lines = []
    for line in yaml_text.splitlines():
        # Match "key: value" (handles keys with dashes like 'package-name')
        match = re.match(r'^(\s*[\w-]+):\s*(.*)$', line)
        if match:
            key, val = match.groups()
            val_s = val.strip()
            # If value contains @ and isn't already quoted, wrap the whole string in double quotes
            if '@' in val_s and not (val_s.startswith('"') or val_s.startswith("'")):
                # Escape any existing double quotes within the value string
                safe_val = val_s.replace('"', '\\"')
                line = f'{key}: "{safe_val}"'
        sanitized_lines.append(line)
    
    sanitized_yaml = '\n'.join(sanitized_lines)
    
    try:
        parsed = yaml.safe_load(sanitized_yaml) or {}
        parsed = normalize_yaml_value(parsed)
        if not isinstance(parsed, Mapping):
            print("⚠️ YAML frontmatter must be a mapping/object")
            return {}
        return dict(parsed)
    except yaml.YAMLError as e:
        print(f"⚠️ YAML parsing error: {e}")
        return {}

def generate_index(skills_dir, output_file, compatibility_report=None):
    print(f"🏗️ Generating index from: {skills_dir}")
    skills = []
    if compatibility_report is None:
        compatibility_report = build_plugin_compatibility_report(pathlib.Path(skills_dir))
    compatibility_lookup = plugin_compatibility_by_path(compatibility_report)

    for root, dirs, files in os.walk(skills_dir):
        # Skip .disabled or hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        if "SKILL.md" in files:
            skill_path = os.path.join(root, "SKILL.md")
            if os.path.islink(skill_path):
                print(f"⚠️ Skipping symlinked SKILL.md: {skill_path}")
                continue
            dir_name = os.path.basename(root)
            parent_dir = os.path.basename(os.path.dirname(root))
            
            # Default values
            rel_path = os.path.relpath(root, os.path.dirname(skills_dir))
            # Force forward slashes for cross-platform JSON compatibility
            skill_info = {
                "id": dir_name,
                "path": rel_path.replace(os.sep, '/'),
                "category": parent_dir if parent_dir != "skills" else None,  # Will be overridden by frontmatter if present
                "subcategory": None,  # Only populated for the direct-classifier (formerly "uncategorized") set
                "name": dir_name.replace("-", " ").title(),
                "description": "",
                "risk": "unknown",
                "source": "unknown",
                "date_added": None,
                "tags": [],
                "plugin": {
                    "targets": {
                        "codex": "supported",
                        "claude": "supported",
                    },
                    "setup": {
                        "type": "none",
                        "summary": "",
                        "docs": None,
                    },
                    "reasons": [],
                },
            }
            
            try:
                with open(skill_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"⚠️ Error reading {skill_path}: {e}")
                continue

            # Parse Metadata
            metadata = parse_frontmatter(content)
            
            # Merge Metadata (frontmatter takes priority)
            name = coerce_metadata_text(metadata.get("name"))
            description = coerce_metadata_text(metadata.get("description"))
            risk = coerce_metadata_text(metadata.get("risk"))
            source = coerce_metadata_text(metadata.get("source"))
            date_added = coerce_metadata_text(metadata.get("date_added"))
            category = coerce_metadata_text(metadata.get("category"))
            tags = coerce_metadata_tags(metadata.get("tags"))

            if name is not None:
                skill_info["name"] = name
            if description is not None:
                skill_info["description"] = description
            if risk is not None:
                skill_info["risk"] = risk
            if source is not None:
                skill_info["source"] = source
            if date_added is not None:
                skill_info["date_added"] = date_added
            if tags:
                skill_info["tags"] = tags

            # Category: prefer frontmatter, then folder structure, then conservative inference
            if category is not None:
                skill_info["category"] = category
            elif skill_info["category"] is None:
                inferred_category = infer_category(
                    skill_info["id"],
                    skill_info["name"],
                    skill_info["description"],
                )
                skill_info["category"] = inferred_category  # may stay None
            if skill_info["id"] in CURATED_CATEGORY_OVERRIDES:
                skill_info["category"] = CURATED_CATEGORY_OVERRIDES[skill_info["id"]]
            skill_info["category"] = normalize_category(skill_info["category"])

            # Final step: collapse the ~97 legacy fine-grained categories into
            # the confirmed 10-bucket taxonomy. Anything that still has no
            # legacy category at this point (previously "uncategorized") is
            # classified directly against the 10 buckets instead, so the
            # index should never contain "uncategorized" going forward.
            if skill_info["category"] is None:
                skill_info["category"] = infer_new_taxonomy_category(
                    skill_info["id"],
                    skill_info["name"],
                    skill_info["description"],
                )
                # Curated fixes for keyword-classifier misses (see dict docstring).
                if skill_info["id"] in NEW_TAXONOMY_CATEGORY_OVERRIDES:
                    skill_info["category"] = NEW_TAXONOMY_CATEGORY_OVERRIDES[skill_info["id"]]
                # Subcategory pass — scoped to this direct-classifier branch only,
                # so legacy-categorized skills (the TAXONOMY_MAP branch below)
                # keep subcategory=None until their own subcategorization pass.
                skill_info["subcategory"] = infer_subcategory(
                    skill_info["category"],
                    skill_info["id"],
                    skill_info["name"],
                    skill_info["description"],
                )
            else:
                legacy_category = skill_info["category"]
                skill_info["category"] = TAXONOMY_MAP.get(
                    skill_info["category"], skill_info["category"]
                )
                # Curated fixes also apply here — a legacy-routed skill can
                # still have an obviously wrong top-level category (see
                # NEW_TAXONOMY_CATEGORY_OVERRIDES docstring); this dict is
                # id-keyed so it's safe to consult from both branches.
                if skill_info["id"] in NEW_TAXONOMY_CATEGORY_OVERRIDES:
                    skill_info["category"] = NEW_TAXONOMY_CATEGORY_OVERRIDES[skill_info["id"]]
                # Subcategory pass for the legacy-routed set (task 3,
                # 2026-07-23) — reuses the same infer_subcategory() as the
                # direct-classifier branch above, but seeded with the raw
                # pre-TAXONOMY_MAP legacy category as an extra signal.
                skill_info["subcategory"] = infer_subcategory(
                    skill_info["category"],
                    skill_info["id"],
                    skill_info["name"],
                    skill_info["description"],
                    legacy_category=legacy_category,
                )

            plugin_info = compatibility_lookup.get(skill_info["path"])
            if plugin_info:
                skill_info["plugin"] = {
                    "targets": dict(plugin_info["targets"]),
                    "setup": dict(plugin_info["setup"]),
                    "reasons": list(plugin_info["reasons"]),
                }
            
            # Fallback for description if missing in frontmatter (legacy support)
            if not skill_info["description"]:
                body = content
                fm_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
                if fm_match:
                    body = content[fm_match.end():].strip()
                
                # Simple extraction of first non-header paragraph
                lines = body.split('\n')
                desc_lines = []
                for line in lines:
                    if line.startswith('#') or not line.strip():
                        if desc_lines: break
                        continue
                    desc_lines.append(line.strip())
                
                if desc_lines:
                    skill_info["description"] = " ".join(desc_lines)[:250].strip()

            skills.append(skill_info)

    # Disambiguate colliding skill ids by path. Distinct skills that happen to share a
    # basename (e.g. tool sub-commands like status/init/run, or super-code/rust vs a
    # top-level rust) must coexist in the index. A flat top-level skill (skills/<name>)
    # keeps its bare id; deeper duplicates get a path-scoped id (parent__name).
    by_id: dict[str, list] = {}
    for skill in skills:
        by_id.setdefault(skill["id"], []).append(skill)
    for _id, group in by_id.items():
        if len(group) == 1:
            continue
        group.sort(key=lambda s: (s["path"].count("/"), s["path"]))
        keep_bare = group[0]["path"].count("/") == 1  # shallowest is a flat top-level skill
        for skill in group[(1 if keep_bare else 0):]:
            skill["id"] = skill["path"].split("skills/", 1)[-1].replace("/", "__")

    # Post-disambiguation override pass. NEW_TAXONOMY_CATEGORY_OVERRIDES and
    # SUBCATEGORY_OVERRIDES are keyed by each skill's FINAL id, but category/
    # subcategory above were resolved using the pre-scoping bare id (dir_name)
    # — so any override targeting a path-scoped id (parent__name, assigned
    # just above on collision) could never match at that point, since the id
    # hadn't been rewritten yet. Re-apply by final id here so those entries
    # take effect (bug found via independent spot-check, 2026-07-23:
    # "engineering-team__code-reviewer" silently kept its pre-override
    # category because it collided with a bare top-level "code-reviewer").
    for skill in skills:
        if skill["id"] in NEW_TAXONOMY_CATEGORY_OVERRIDES:
            skill["category"] = NEW_TAXONOMY_CATEGORY_OVERRIDES[skill["id"]]
        if skill["id"] in SUBCATEGORY_OVERRIDES:
            skill["subcategory"] = SUBCATEGORY_OVERRIDES[skill["id"]]

    # Safety: ids must be unique after path-scoping
    seen_ids: dict[str, str] = {}
    duplicate_ids: list[tuple[str, str, str]] = []
    for skill in skills:
        existing_path = seen_ids.get(skill["id"])
        if existing_path is not None:
            duplicate_ids.append((skill["id"], existing_path, skill["path"]))
        else:
            seen_ids[skill["id"]] = skill["path"]
    if duplicate_ids:
        details = "; ".join(
            f"{skill_id}: {first_path} conflicts with {second_path}"
            for skill_id, first_path, second_path in duplicate_ids
        )
        raise ValueError(f"Duplicate skill ids after path-scoping: {details}")

    # Safety: subcategory must be a member of SUBCATEGORY_TAXONOMY[category]
    # (or the "General" catch-all). Catches drift such as a SUBCATEGORY_OVERRIDES
    # entry pinned to a subcategory whose id is missing from (or mismatched
    # with) NEW_TAXONOMY_CATEGORY_OVERRIDES.
    invalid_subcats = []
    for skill in skills:
        subcat = skill.get("subcategory")
        if subcat is None:
            continue
        allowed = SUBCATEGORY_TAXONOMY.get(skill["category"], [])
        if subcat != "General" and subcat not in allowed:
            invalid_subcats.append((skill["id"], skill["category"], subcat))
    if invalid_subcats:
        details = "; ".join(f"{i}: category={c!r} subcategory={s!r}" for i, c, s in invalid_subcats)
        raise ValueError(f"Skill subcategory doesn't match its category's taxonomy: {details}")

    # Sort validation: by name
    skills.sort(key=lambda x: (x["name"].lower(), x["id"].lower()))

    with open(output_file, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(skills, f, indent=2)
    
    print(f"✅ Generated rich index with {len(skills)} skills at: {output_file}")
    return skills

def mirror_canonical_index(output_path):
    """Mirror the root public manifest into data/ for compatibility consumers."""
    output_path = pathlib.Path(output_path)
    root = pathlib.Path(find_repo_root(__file__))
    root_index = root / "skills_index.json"
    if output_path.resolve() != root_index.resolve():
        return None

    data_index = root / "data" / "skills_index.json"
    data_index.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(output_path, data_index)
    print(f"✅ Mirrored canonical index to: {data_index}")
    return data_index

if __name__ == "__main__":
    base_dir = str(find_repo_root(__file__))
    skills_path = os.path.join(base_dir, "skills")
    output_path = os.path.join(base_dir, "skills_index.json")
    generate_index(skills_path, output_path)
    mirror_canonical_index(output_path)
