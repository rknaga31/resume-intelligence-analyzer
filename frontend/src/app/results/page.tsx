"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import type { FullAnalysisResponse } from "@/lib/api";
import { scoreToColor, scoreToGrade, scoreToRingColor } from "@/lib/utils";

// ── Reusable UI helpers ──────────────────────────────────────────────────────

function ScoreRing({
  score,
  label,
  size = 110,
}: {
  score: number;
  label: string;
  size?: number;
}) {
  const r = size / 2 - 10;
  const circumference = 2 * Math.PI * r;
  const offset = circumference * (1 - score / 100);
  const cx = size / 2;
  const cy = size / 2;
  const ringColor = scoreToRingColor(score);

  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="-rotate-90">
          <circle
            cx={cx}
            cy={cy}
            r={r}
            fill="none"
            stroke="rgba(255,255,255,0.08)"
            strokeWidth="8"
          />
          <circle
            cx={cx}
            cy={cy}
            r={r}
            fill="none"
            strokeWidth="8"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            className={ringColor}
            style={{ transition: "stroke-dashoffset 0.8s cubic-bezier(0.4,0,0.2,1)" }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={`text-2xl font-bold ${scoreToColor(score)}`}>{score}</span>
          <span className="text-[10px] text-gray-500 uppercase tracking-wide">{scoreToGrade(score)}</span>
        </div>
      </div>
      <span className="text-xs text-gray-400 text-center max-w-[90px]">{label}</span>
    </div>
  );
}

function Section({
  title,
  icon,
  children,
}: {
  title: string;
  icon: string;
  children: React.ReactNode;
}) {
  return (
    <div className="glass-card p-6">
      <h2 className="text-lg font-semibold flex items-center gap-2 mb-5">
        <span>{icon}</span>
        {title}
      </h2>
      {children}
    </div>
  );
}

function SkillPill({
  label,
  type,
}: {
  label: string;
  type: "matched" | "partial" | "missing";
}) {
  const styles = {
    matched: "bg-emerald-500/15 border-emerald-500/30 text-emerald-300",
    partial: "bg-yellow-500/15 border-yellow-500/30 text-yellow-300",
    missing: "bg-red-500/15 border-red-500/30 text-red-300",
  };
  return (
    <span
      className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium border ${styles[type]}`}
    >
      {label}
    </span>
  );
}

function ProgressBar({ value, color = "bg-violet-500" }: { value: number; color?: string }) {
  return (
    <div className="w-full h-2 bg-white/10 rounded-full overflow-hidden">
      <div
        className={`h-full ${color} rounded-full transition-all duration-700`}
        style={{ width: `${value}%` }}
      />
    </div>
  );
}

// ── Main Results Page ────────────────────────────────────────────────────────

export default function ResultsPage() {
  const router = useRouter();
  const [data, setData] = useState<FullAnalysisResponse | null>(null);
  const [targetRole, setTargetRole] = useState("");

  useEffect(() => {
    const stored = sessionStorage.getItem("analysisResult");
    const role = sessionStorage.getItem("targetRole") ?? "";
    if (!stored) {
      router.push("/analyze");
      return;
    }
    setData(JSON.parse(stored) as FullAnalysisResponse);
    setTargetRole(role);
  }, [router]);

  if (!data) {
    return (
      <main className="min-h-screen flex items-center justify-center">
        <div className="text-gray-500">Loading results…</div>
      </main>
    );
  }

  const { scores, skills, achievement_analysis, llm_synthesis, sections_found } = data;

  return (
    <main className="min-h-screen pb-20">
      {/* Header bar */}
      <div className="sticky top-0 z-40 border-b border-white/5 bg-gray-950/80 backdrop-blur-xl">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3 min-w-0">
            <Link href="/" className="text-xl shrink-0">🧠</Link>
            <span className="text-sm text-gray-400 truncate">
              Analysis for <span className="text-white font-medium">{targetRole || data.target_role}</span>
            </span>
          </div>
          <div className="flex items-center gap-3 shrink-0">
            <span className="text-xs text-gray-600 hidden sm:block">ID: {data.analysis_id}</span>
            <Link href="/analyze" className="btn-secondary text-xs !py-2 !px-4">
              New Analysis
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 pt-8 space-y-6">
        {/* Overall score hero */}
        <div className="glass-card p-8 animate-fade-up">
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-8 items-center">
            <div className="col-span-2 sm:col-span-1 flex justify-center sm:justify-start">
              <ScoreRing score={scores.overall_score} label="Overall Score" size={130} />
            </div>
            <div className="col-span-2 sm:col-span-3 grid grid-cols-1 sm:grid-cols-3 gap-6">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs text-gray-400">ATS Compatibility</span>
                  <span className={`text-sm font-bold ${scoreToColor(scores.ats_compatibility_score)}`}>
                    {scores.ats_compatibility_score}
                  </span>
                </div>
                <ProgressBar
                  value={scores.ats_compatibility_score}
                  color={scores.ats_compatibility_score >= 80 ? "bg-emerald-500" : scores.ats_compatibility_score >= 60 ? "bg-yellow-500" : "bg-red-500"}
                />
              </div>
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs text-gray-400">Job Match</span>
                  <span className={`text-sm font-bold ${scoreToColor(scores.job_match_score)}`}>
                    {scores.job_match_score}
                  </span>
                </div>
                <ProgressBar
                  value={scores.job_match_score}
                  color={scores.job_match_score >= 80 ? "bg-emerald-500" : scores.job_match_score >= 60 ? "bg-yellow-500" : "bg-red-500"}
                />
              </div>
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs text-gray-400">Achievement Impact</span>
                  <span className={`text-sm font-bold ${scoreToColor(scores.achievement_impact_score)}`}>
                    {scores.achievement_impact_score}
                  </span>
                </div>
                <ProgressBar
                  value={scores.achievement_impact_score}
                  color={scores.achievement_impact_score >= 80 ? "bg-emerald-500" : scores.achievement_impact_score >= 60 ? "bg-yellow-500" : "bg-red-500"}
                />
              </div>
            </div>
          </div>

          {/* ATS disclaimer */}
          <p className="mt-6 text-[11px] text-gray-600 border-t border-white/5 pt-4">
            ⚠️ {scores.ats_disclaimer}
          </p>
        </div>

        {/* Executive Summary */}
        <Section title="Executive Summary" icon="📋">
          <p className="text-gray-300 leading-relaxed">{llm_synthesis.executive_summary}</p>
          <p className="text-xs text-gray-600 mt-3">
            Analysis provider: <span className="text-gray-500 font-mono">{llm_synthesis.provider_used}</span>
          </p>
        </Section>

        {/* Skills — 2 col grid */}
        <div className="grid lg:grid-cols-2 gap-6">
          {/* Skill match breakdown */}
          <Section title="Skill Match Analysis" icon="🎯">
            <div className="space-y-5">
              {skills.matched.length > 0 && (
                <div>
                  <div className="flex items-center gap-2 mb-3">
                    <span className="w-2 h-2 rounded-full bg-emerald-400" />
                    <span className="text-xs text-gray-400 font-medium uppercase tracking-wide">
                      Matched ({skills.matched.length})
                    </span>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {skills.matched.map((s) => (
                      <SkillPill key={s} label={s} type="matched" />
                    ))}
                  </div>
                </div>
              )}

              {skills.partial.length > 0 && (
                <div>
                  <div className="flex items-center gap-2 mb-3">
                    <span className="w-2 h-2 rounded-full bg-yellow-400" />
                    <span className="text-xs text-gray-400 font-medium uppercase tracking-wide">
                      Related / Partial ({skills.partial.length})
                    </span>
                  </div>
                  <div className="space-y-2">
                    {skills.partial.map((p, i) => (
                      <div key={i} className="flex items-center gap-2 text-xs">
                        <SkillPill label={p.resume_skill} type="partial" />
                        <span className="text-gray-600">↔</span>
                        <SkillPill label={p.job_skill} type="partial" />
                        <span className="text-gray-600 ml-auto">{Math.round(p.similarity * 100)}% related</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {skills.missing.length > 0 && (
                <div>
                  <div className="flex items-center gap-2 mb-3">
                    <span className="w-2 h-2 rounded-full bg-red-400" />
                    <span className="text-xs text-gray-400 font-medium uppercase tracking-wide">
                      Missing ({skills.missing.length})
                    </span>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {skills.missing.map((s) => (
                      <SkillPill key={s} label={s} type="missing" />
                    ))}
                  </div>
                </div>
              )}

              {skills.matched.length === 0 && skills.missing.length === 0 && (
                <p className="text-sm text-gray-500">
                  Add a job description to see detailed skill gap analysis.
                </p>
              )}
            </div>
          </Section>

          {/* Resume skills */}
          <Section title="Your Skills Detected" icon="🗂️">
            <div className="flex flex-wrap gap-2">
              {skills.resume_skills.length > 0
                ? skills.resume_skills.map((s) => (
                    <span
                      key={s}
                      className="px-3 py-1 rounded-full text-xs bg-violet-500/15 border border-violet-500/20 text-violet-300"
                    >
                      {s}
                    </span>
                  ))
                : <p className="text-sm text-gray-500">No skills detected in taxonomy. Try a more detailed resume.</p>}
            </div>
          </Section>
        </div>

        {/* Strengths & Weaknesses */}
        <div className="grid lg:grid-cols-2 gap-6">
          <Section title="Strengths" icon="✅">
            <ul className="space-y-3">
              {llm_synthesis.strengths.map((s, i) => (
                <li key={i} className="flex items-start gap-3 text-sm text-gray-300">
                  <span className="text-emerald-400 mt-0.5 shrink-0">+</span>
                  {s}
                </li>
              ))}
            </ul>
          </Section>
          <Section title="Areas to Improve" icon="⚠️">
            <ul className="space-y-3">
              {llm_synthesis.weaknesses.map((w, i) => (
                <li key={i} className="flex items-start gap-3 text-sm text-gray-300">
                  <span className="text-orange-400 mt-0.5 shrink-0">!</span>
                  {w}
                </li>
              ))}
            </ul>
          </Section>
        </div>

        {/* Achievement Analysis */}
        <Section title="Achievement Impact Analysis" icon="📈">
          <div className="flex items-center gap-6 mb-6">
            <div className="text-center">
              <div className={`text-3xl font-bold ${scoreToColor(achievement_analysis.quantified_bullets_count / Math.max(achievement_analysis.total_bullets_count, 1) >= 0.7 ? 90 : achievement_analysis.quantified_bullets_count / Math.max(achievement_analysis.total_bullets_count, 1) >= 0.5 ? 75 : 40)}`}>
                {achievement_analysis.quantified_bullets_count}/{achievement_analysis.total_bullets_count}
              </div>
              <div className="text-xs text-gray-500 mt-1">bullets quantified</div>
            </div>
            <div className="flex-1">
              <div className="flex justify-between mb-1">
                <span className="text-xs text-gray-400">Quantification rate</span>
                <span className="text-xs font-medium text-white">{Math.round(achievement_analysis.quantification_rate * 100)}%</span>
              </div>
              <ProgressBar
                value={achievement_analysis.quantification_rate * 100}
                color={achievement_analysis.quantification_rate >= 0.7 ? "bg-emerald-500" : achievement_analysis.quantification_rate >= 0.5 ? "bg-yellow-500" : "bg-red-500"}
              />
            </div>
          </div>

          {achievement_analysis.bullet_feedback.length > 0 && (
            <div className="space-y-4">
              <h3 className="text-sm font-medium text-gray-300">Bullet Improvement Suggestions</h3>
              {achievement_analysis.bullet_feedback.map((bf, i) => (
                <div key={i} className="rounded-xl border border-white/5 bg-white/[0.03] p-4 space-y-2">
                  <p className="text-xs text-gray-500">Original:</p>
                  <p className="text-sm text-gray-400 italic">"{bf.original}"</p>
                  <p className="text-xs text-orange-400">⚠️ {bf.issue}</p>
                  <p className="text-xs text-emerald-400">💡 {bf.suggestion}</p>
                </div>
              ))}
            </div>
          )}
        </Section>

        {/* Recommendations & Roadmap */}
        <div className="grid lg:grid-cols-2 gap-6">
          <Section title="Actionable Recommendations" icon="🎯">
            <ol className="space-y-3 list-none">
              {llm_synthesis.actionable_recommendations.map((rec, i) => (
                <li key={i} className="flex items-start gap-3 text-sm text-gray-300">
                  <span className="shrink-0 text-xs font-mono text-violet-400 mt-0.5 w-5">
                    {i + 1}.
                  </span>
                  {rec}
                </li>
              ))}
            </ol>
          </Section>
          <Section title="Career Roadmap" icon="🗺️">
            <ol className="space-y-3 relative">
              <div className="absolute left-2.5 top-2 bottom-2 w-px bg-white/10" />
              {llm_synthesis.career_roadmap.map((step, i) => (
                <li key={i} className="flex items-start gap-4 text-sm text-gray-300 relative pl-7">
                  <div className="absolute left-0 top-0.5 w-5 h-5 rounded-full border border-violet-500/40 bg-violet-500/10 flex items-center justify-center shrink-0">
                    <span className="text-[10px] text-violet-400 font-bold">{i + 1}</span>
                  </div>
                  {step}
                </li>
              ))}
            </ol>
          </Section>
        </div>

        {/* Resume metadata */}
        <Section title="Resume Structure Analysis" icon="📑">
          <div className="grid sm:grid-cols-2 gap-4">
            <div>
              <p className="text-xs text-gray-500 mb-2">Sections Detected</p>
              <div className="flex flex-wrap gap-2">
                {sections_found.map((s) => (
                  <span key={s} className="px-2 py-1 rounded-md bg-white/5 border border-white/10 text-xs text-gray-300">
                    {s}
                  </span>
                ))}
              </div>
            </div>
            <div>
              <p className="text-xs text-gray-500 mb-2">Score Components</p>
              <div className="grid grid-cols-2 gap-3">
                {[
                  { label: "ATS", v: scores.ats_compatibility_score },
                  { label: "Job Match", v: scores.job_match_score },
                  { label: "Achievements", v: scores.achievement_impact_score },
                  { label: "Skills", v: scores.skill_relevance_score },
                ].map(({ label, v }) => (
                  <div key={label} className="text-center py-2 px-3 rounded-lg bg-white/[0.03] border border-white/5">
                    <div className={`text-lg font-bold ${scoreToColor(v)}`}>{v}</div>
                    <div className="text-xs text-gray-600">{label}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </Section>

        {/* CTA */}
        <div className="text-center py-8">
          <Link href="/analyze" className="btn-primary text-base !py-3.5 !px-8">
            Analyze Another Resume →
          </Link>
        </div>
      </div>
    </main>
  );
}
