# Frontend — Resume Intelligence Analyzer

React & Next.js web application for the **Resume Intelligence Analyzer**, delivering an interactive dashboard for resume analysis, skill gap visualization, ATS compatibility scoring, and AI bullet point optimization.

---

## Directory Structure

```
frontend/
├── src/
│   ├── app/                  # Next.js App Router pages
│   │   ├── layout.tsx        # Root layout with dark mode glassmorphism
│   │   ├── page.tsx          # Landing page with hero & features
│   │   ├── analyze/          # Interactive resume upload & job input page
│   │   └── results/          # Full intelligence dashboard & score breakdown
│   ├── components/           # Reusable UI components
│   │   ├── ui/               # Base UI elements
│   │   └── analysis/         # Analysis visualization components
│   └── lib/
│       ├── api.ts            # Centralized API client (`apiClient`)
│       └── utils.ts          # Shared utility functions (`cn`, formatting)
├── public/                   # Static branding assets
├── package.json              # Project dependencies & scripts
├── tsconfig.json             # TypeScript configuration (strict mode)
├── next.config.ts            # Next.js build configuration
└── Dockerfile                # Multi-stage production container build
```

---

## Technology Stack

- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript 5+ (Strict Mode)
- **Styling**: Tailwind CSS with custom glassmorphism design system
- **State & API**: Centralized `apiClient` (`frontend/src/lib/api.ts`) connecting to FastAPI backend
- **Icons**: Lucide React icons

---

## Getting Started

### Development Mode

```bash
# Install dependencies
npm install

# Run development server (http://localhost:3000)
npm run dev
```

### Production Build

```bash
# Run TypeScript & Next.js production build
npm run build

# Start production server
npm run start
```

---

## Quality & Standards

- **TypeScript**: Strictly typed components and API response definitions
- **Linting**: Enforced via `eslint` and `next lint`
- **Docker**: Containerized deployment via `Dockerfile` and `docker-compose.yml`

See [AGENTS.md](../AGENTS.md) for root development standards.
