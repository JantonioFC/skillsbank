# Acceptance Criteria for aspire-ts Skill

## Skill Activation

- [ ] Skill activates when user asks about orchestrating JS/TS apps with Aspire
- [ ] Skill activates when user mentions Vite, Node.js, React, Vue, Svelte + Aspire
- [ ] Skill activates when user asks about `AddViteApp`, `AddNodeApp`, `AddJavaScriptApp`

## Core Patterns

- [ ] AppHost correctly uses `Aspire.Hosting.JavaScript` package
- [ ] File-based AppHost uses `#:package` directive syntax
- [ ] `AddViteApp` used for Vite-based frontends (React, Vue, Svelte)
- [ ] `AddNodeApp` used for Node.js servers with direct file entry
- [ ] `AddJavaScriptApp` used for generic JS apps with npm scripts
- [ ] Package manager specified with `.WithNpm()`, `.WithYarn()`, or `.WithPnpm()`

## Service Discovery

- [ ] `.WithReference()` correctly injects environment variables
- [ ] JS/TS code reads correct env var names (`{NAME}_HTTP`, `{NAME}_HOST`, etc.)
- [ ] Connection strings use `ConnectionStrings__{name}` format where applicable

## Endpoints

- [ ] `.WithHttpEndpoint(port, env: "PORT")` correctly configures port + env var
- [ ] `.WithExternalHttpEndpoints()` used for browser-facing apps
- [ ] Health checks configured with `.WithHttpHealthCheck("/health")`
- [ ] HTTPS configured with `.WithHttpsDeveloperCertificate()` when needed

## Telemetry

- [ ] OpenTelemetry setup imports `telemetry.js` before all other imports
- [ ] Uses `OTEL_EXPORTER_OTLP_ENDPOINT` from environment (auto-set by Aspire)
- [ ] Auto-instrumentations configured for HTTP, Express, database clients
- [ ] Graceful shutdown handler included

## Deployment

- [ ] Production builds use deterministic install (`npm ci`, `yarn --immutable`, etc.)
- [ ] Lockfiles assumed to be committed
- [ ] Container registry integration properly configured
- [ ] GitHub Actions workflow uses correct parameter env var naming

## Azure Integration

- [ ] `.RunAsContainer()` used for local development with Azure resources
- [ ] `.RunAsEmulator()` used for emulatable services (Storage, Service Bus, etc.)
- [ ] Correct Azure SDK packages imported in Node.js consuming code
- [ ] Connection strings accessed via correct env var names

## Anti-Patterns to Avoid

- [ ] Never suggest writing AppHost in JavaScript/TypeScript (it's always C#)
- [ ] Never hardcode connection strings in JS/TS code
- [ ] Never skip lockfile in production builds
- [ ] Never import application code before telemetry setup
- [ ] Never use deprecated `AddNpmApp` API (use `AddJavaScriptApp` or `AddViteApp`)
