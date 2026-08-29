import Link from "next/link";

const features = [
  {
    icon: "🧠",
    title: "Deterministic NLP Pipeline",
    desc: "Section detection, entity extraction, and skill taxonomy—not a simple LLM wrapper.",
  },
  {
    icon: "🎯",
    title: "Semantic Job Matching",
    desc: "Transformer embeddings compute real similarity between your experience and job requirements.",
  },
  {
    icon: "📊",
    title: "Explainable Scores",
    desc: "Every score has evidence, methodology, and improvement guidance—no black boxes.",
  },
  {
    icon: "⚡",
    title: "Achievement Impact Audit",
    desc: "Detects quantified bullets (%, $, scale, latency) and flags weak ones with specific suggestions.",
  },
  {
    icon: "🛡️",
    title: "Prompt Injection Defense",
    desc: "Resume content is sandboxed—embedded instructions in documents cannot hijack the AI.",
  },
  {
    icon: "🔒",
    title: "Privacy First",
    desc: "Resumes are processed in-memory and never stored permanently. Zero PII in logs.",
  },
];

const steps = [
  { num: "01", title: "Upload Resume", desc: "PDF, DOCX, or TXT. Validated by magic bytes, not just filename." },
  { num: "02", title: "Select Target Role", desc: "Specify your target job and optionally paste a full job description." },
  { num: "03", title: "Intelligence Pipeline", desc: "NLP extraction → skill taxonomy → semantic embeddings → deterministic scoring." },
  { num: "04", title: "Review Dashboard", desc: "Multi-dimensional scores, skill gaps (matched/partial/missing), and LLM recommendations." },
];

const faqs = [
  {
    q: "Is this a real ATS system?",
    a: "No. This is an AI-assisted ATS-style compatibility analysis. It does not replicate or guarantee the behavior of any specific employer's proprietary ATS system.",
  },
  {
    q: "Is my resume stored?",
    a: "No. Resumes are processed entirely in-memory and deleted immediately after analysis. We never store your resume text or personal information.",
  },
  {
    q: "Does the AI make up scores?",
    a: "No. Scores are computed by deterministic NLP algorithms. The LLM only generates the narrative explanations and recommendations.",
  },
  {
    q: "Which LLM providers are supported?",
    a: "Google Gemini, OpenAI, and Anthropic. The system also includes a rule-based fallback that works without any LLM API key.",
  },
];

export default function LandingPage() {
  return (
    <main className="min-h-screen">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 border-b border-white/5 bg-gray-950/80 backdrop-blur-xl">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-2xl">🧠</span>
            <span className="font-bold text-lg tracking-tight gradient-text">
              ResumeIQ
            </span>
          </div>
          <div className="flex items-center gap-6">
            <a href="#how-it-works" className="text-sm text-gray-400 hover:text-white transition-colors hidden sm:block">
              How it works
            </a>
            <a href="#features" className="text-sm text-gray-400 hover:text-white transition-colors hidden sm:block">
              Features
            </a>
            <a href="#privacy" className="text-sm text-gray-400 hover:text-white transition-colors hidden sm:block">
              Privacy
            </a>
            <Link href="/analyze" className="btn-primary text-sm !py-2 !px-4">
              Analyze Resume →
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative overflow-hidden pt-24 pb-32">
        {/* Background glow */}
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full bg-violet-600/10 blur-3xl" />
          <div className="absolute top-1/3 left-1/3 w-[300px] h-[300px] rounded-full bg-cyan-600/8 blur-3xl" />
        </div>

        <div className="relative max-w-4xl mx-auto px-6 text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-violet-500/30 bg-violet-500/10 text-violet-300 text-sm font-medium mb-8">
            <span className="w-1.5 h-1.5 rounded-full bg-violet-400 animate-pulse" />
            AI-Powered Resume Intelligence
          </div>

          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight text-balance mb-6">
            Understand How Your{" "}
            <span className="gradient-text">Resume Performs</span>
          </h1>

          <p className="text-xl text-gray-400 max-w-2xl mx-auto mb-10 text-balance leading-relaxed">
            Upload your resume, compare it against a target role, identify skill gaps,
            and receive actionable AI-powered recommendations backed by real NLP analysis—not guesswork.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/analyze" className="btn-primary text-base !py-3.5 !px-8 animate-pulse-glow">
              Analyze My Resume →
            </Link>
            <a
              href="http://localhost:8000/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="btn-secondary text-base !py-3.5 !px-8"
            >
              View API Docs
            </a>
          </div>

          {/* Disclaimer */}
          <p className="mt-8 text-xs text-gray-600 max-w-lg mx-auto">
            Privacy-first: resumes are processed in-memory and never stored.
            ATS-style scores do not represent any specific employer&apos;s system.
          </p>
        </div>
      </section>

      {/* How it works */}
      <section id="how-it-works" className="py-24 border-t border-white/5">
        <div className="max-w-6xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold mb-4">How It Works</h2>
            <p className="text-gray-400 max-w-xl mx-auto">
              A deterministic multi-stage intelligence pipeline—not a simple prompt-to-LLM wrapper.
            </p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {steps.map((step, i) => (
              <div key={i} className="glass-card p-6 relative">
                <div className="text-4xl font-bold text-violet-500/30 mb-3 font-mono">
                  {step.num}
                </div>
                <h3 className="font-semibold text-white mb-2">{step.title}</h3>
                <p className="text-sm text-gray-400 leading-relaxed">{step.desc}</p>
                {i < steps.length - 1 && (
                  <div className="hidden lg:block absolute -right-3 top-1/2 -translate-y-1/2 text-gray-700 text-xl">
                    →
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* AI Pipeline */}
      <section className="py-24 border-t border-white/5 bg-white/[0.02]">
        <div className="max-w-6xl mx-auto px-6">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl font-bold mb-4">The Intelligence Pipeline</h2>
              <p className="text-gray-400 mb-8 leading-relaxed">
                Unlike tools that simply forward your resume to an LLM and return whatever it says,
                ResumeIQ runs a structured multi-stage pipeline where every score is derived from
                deterministic algorithms with documented methodology.
              </p>
              <div className="space-y-3">
                {[
                  ["📄", "Document Processing", "MIME & magic-byte validation, multi-backend PDF/DOCX extraction"],
                  ["🔍", "Section Detection", "15+ canonical sections, 50+ header variations"],
                  ["🏷️", "Entity Extraction", "Name, contact, education, experience, projects"],
                  ["🗂️", "Skill Taxonomy", "250+ skills across 13 categories with alias matching"],
                  ["📐", "Semantic Embeddings", "Transformer vector similarity (all-MiniLM-L6-v2)"],
                  ["📊", "Explainable Scoring", "ATS, job match, achievement impact, skill relevance"],
                  ["🤖", "LLM Reasoning", "Sandboxed synthesis with prompt injection defense"],
                ].map(([icon, title, desc], i) => (
                  <div key={i} className="flex items-start gap-3">
                    <span className="text-lg mt-0.5">{icon}</span>
                    <div>
                      <span className="font-medium text-white">{title}</span>
                      <span className="text-gray-500 text-sm"> — {desc}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <div className="glass-card p-6 font-mono text-sm">
              <div className="text-violet-400 mb-2"># Pipeline output example</div>
              <pre className="text-gray-300 text-xs leading-relaxed overflow-auto">{`{
  "scores": {
    "overall_score": 88,
    "ats_compatibility_score": 92,
    "job_match_score": 85,
    "achievement_impact_score": 91
  },
  "skills": {
    "matched": ["python", "pytorch", "docker"],
    "partial": [{
      "resume_skill": "tensorflow",
      "job_skill": "pytorch",
      "similarity": 0.85
    }],
    "missing": ["aws", "kubernetes"]
  },
  "achievement_analysis": {
    "quantification_rate": 0.75,
    "bullet_feedback": [{
      "original": "Built ML pipeline.",
      "issue": "Lacks measurable outcome",
      "suggestion": "Add scale, latency, or accuracy metric."
    }]
  }
}`}</pre>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-24 border-t border-white/5">
        <div className="max-w-6xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold mb-4">Built for Engineers, by Engineers</h2>
            <p className="text-gray-400 max-w-xl mx-auto">
              Production-quality engineering behind every analysis.
            </p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((f, i) => (
              <div
                key={i}
                className="glass-card p-6 hover:border-violet-500/30 hover:bg-white/[0.07] transition-all duration-200 group"
              >
                <div className="text-3xl mb-4">{f.icon}</div>
                <h3 className="font-semibold text-white mb-2 group-hover:text-violet-300 transition-colors">
                  {f.title}
                </h3>
                <p className="text-sm text-gray-400 leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Privacy */}
      <section id="privacy" className="py-24 border-t border-white/5 bg-white/[0.02]">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <div className="text-4xl mb-6">🔒</div>
          <h2 className="text-3xl font-bold mb-4">Privacy by Design</h2>
          <p className="text-gray-400 text-lg mb-8 max-w-2xl mx-auto leading-relaxed">
            Resumes contain sensitive personal information. ResumeIQ is engineered with strict privacy principles:
          </p>
          <div className="grid sm:grid-cols-3 gap-6 text-left">
            {[
              { title: "Zero Persistent Storage", desc: "Your resume is processed in-memory only. No files are written to disk or retained after analysis." },
              { title: "Zero PII in Logs", desc: "Application logs contain only technical metadata—never your name, email, phone, or resume text." },
              { title: "Sandboxed AI Prompts", desc: "Resume content is isolated inside explicit boundary tags. Embedded instructions cannot affect AI behavior." },
            ].map((item, i) => (
              <div key={i} className="glass-card p-5">
                <h3 className="font-semibold text-white mb-2">{item.title}</h3>
                <p className="text-sm text-gray-400 leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="py-24 border-t border-white/5">
        <div className="max-w-3xl mx-auto px-6">
          <h2 className="text-3xl font-bold text-center mb-12">Frequently Asked Questions</h2>
          <div className="space-y-4">
            {faqs.map((faq, i) => (
              <div key={i} className="glass-card p-6">
                <h3 className="font-semibold text-white mb-2">{faq.q}</h3>
                <p className="text-sm text-gray-400 leading-relaxed">{faq.a}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-24 border-t border-white/5">
        <div className="max-w-3xl mx-auto px-6 text-center">
          <h2 className="text-4xl font-bold mb-6 text-balance">
            Ready to Understand Your{" "}
            <span className="gradient-text">Resume&apos;s Strengths?</span>
          </h2>
          <p className="text-gray-400 text-lg mb-10">
            Free to use. No account required. Results in seconds.
          </p>
          <Link href="/analyze" className="btn-primary text-lg !py-4 !px-10">
            Analyze My Resume →
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/5 py-8">
        <div className="max-w-6xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <span>🧠</span>
            <span className="font-semibold gradient-text">ResumeIQ</span>
          </div>
          <p className="text-xs text-gray-600 text-center">
            ATS-style analysis does not guarantee the behavior of any specific employer&apos;s system.
            Resumes are never stored. © 2026 rknaga31.
          </p>
          <a
            href="https://github.com/rknaga31/resume-intelligence-analyzer"
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs text-gray-500 hover:text-white transition-colors"
          >
            GitHub →
          </a>
        </div>
      </footer>
    </main>
  );
}
