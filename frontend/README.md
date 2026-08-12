# frontend/

React / Next.js frontend application for the Resume Intelligence Analyzer.

## Planned Structure

```
frontend/
├── src/
│   ├── app/                  # Next.js App Router pages
│   │   ├── layout.tsx        # Root layout
│   │   ├── page.tsx          # Landing page
│   │   ├── upload/           # Resume upload flow
│   │   └── dashboard/        # Analysis results dashboard
│   ├── components/
│   │   ├── ui/               # Primitive UI components
│   │   ├── upload/           # Upload-specific components
│   │   └── analysis/         # Analysis result components
│   ├── hooks/                # Custom React hooks
│   ├── lib/
│   │   ├── api.ts            # Centralized API client
│   │   └── utils.ts          # Shared utilities
│   └── types/                # TypeScript type definitions
├── public/                   # Static assets
├── package.json
├── tsconfig.json
├── next.config.ts
└── Dockerfile
```

## Technology

- Next.js 14+ (App Router)
- TypeScript 5+ (strict mode)
- React 18+
- Tailwind CSS
- ESLint + Prettier

See [AGENTS.md](../AGENTS.md) for coding standards.
