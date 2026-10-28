# Healthcare Operations & Patient Analytics

An end-to-end healthcare analytics workspace that turns synthetic hospital activity into operational, financial, patient, and readmission insights.

## Run & Operate

- `pnpm --filter @workspace/api-server run dev` — run the API server (port 5000)
- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from the OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- Required env: `DATABASE_URL` — Postgres connection string

## Stack

- pnpm workspaces, Node.js 24, TypeScript 5.9
- API: Express 5
- DB: PostgreSQL + Drizzle ORM
- Validation: Zod (`zod/v4`), `drizzle-zod`
- API codegen: Orval (from OpenAPI spec)
- Build: esbuild (CJS bundle)

## Where things live

- `artifacts/healthcare-analytics/` — runnable dashboard and visual analytics experience.
- `artifacts/api-server/src/routes/healthcare.ts` — healthcare API route source.
- `artifacts/api-server/data/seed_healthcare.sql` — deterministic synthetic portfolio dataset.
- `lib/db/src/schema/healthcare.ts` — relational source-of-truth schema.
- `lib/api-spec/openapi.yaml` — source-of-truth API contract.
- `analytics/` — SQL business questions, Python cleaning/ML scripts, Excel checklist, and data dictionary.

## Architecture decisions

- The dataset is synthetic and deterministic so the dashboard, SQL, Python, and Power BI layers can use the same repeatable source.
- The relational model separates patients, admissions, departments, doctors, treatments, billing, and lab results rather than relying on one denormalized CSV.
- The readmission model is an explainable logistic-regression baseline for portfolio analysis, not a clinical decision system.
- Dashboard metrics are exposed through the shared API so the UI, SQL questions, and future Power BI model stay aligned.

## Product

The dashboard presents executive KPIs, monthly admissions and readmission trends, department workload and cost, condition cost profile, readmission factor segments, and a recent admissions worklist. It supports refresh controls, dark mode, print/PDF output, and CSV exports for chart data.

## User preferences

- Keep the project realistic and interview-defensible; do not add technologies without a clear analytics purpose.
- Use Excel for inspection, Python/Pandas for repeatable cleaning and feature engineering, SQL for relational analysis, and ML only for a focused readmission baseline.

## Gotchas

- The API server depends on the development PostgreSQL schema and seeded synthetic data.
- After changing `lib/api-spec/openapi.yaml`, regenerate clients with `pnpm --filter @workspace/api-spec run codegen`.

## Pointers

- See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details
