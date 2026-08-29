"use client";

import { useState, useCallback, useRef } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { apiClient, type FullAnalysisResponse } from "@/lib/api";
import { formatBytes } from "@/lib/utils";

const POPULAR_ROLES = [
  "Senior Software Engineer",
  "Senior AI / ML Engineer",
  "Data Scientist",
  "Full Stack Engineer",
  "DevOps / Platform Engineer",
  "Product Manager",
  "Data Engineer",
  "Machine Learning Researcher",
  "Backend Engineer",
  "Frontend Engineer",
];

type Step = "upload" | "configure" | "analyzing";

export default function AnalyzePage() {
  const router = useRouter();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [step, setStep] = useState<Step>("upload");
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [extractedText, setExtractedText] = useState<string>("");
  const [wordCount, setWordCount] = useState(0);
  const [targetRole, setTargetRole] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [dragOver, setDragOver] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [analyzeProgress, setAnalyzeProgress] = useState(0);

  const analyzeSteps = [
    "Extracting document text…",
    "Detecting sections…",
    "Classifying skills…",
    "Computing semantic embeddings…",
    "Scoring ATS compatibility…",
    "Analyzing achievements…",
    "Synthesizing recommendations…",
  ];
  const [progressStep, setProgressStep] = useState(0);

  const handleFile = useCallback(async (file: File) => {
    setError(null);
    setUploading(true);
    try {
      const result = await apiClient.uploadResume(file);
      setUploadedFile(file);
      setExtractedText(result.extracted_text);
      setWordCount(result.word_count);
      setStep("configure");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Upload failed. Please try again.");
    } finally {
      setUploading(false);
    }
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setDragOver(false);
      const file = e.dataTransfer.files[0];
      if (file) handleFile(file);
    },
    [handleFile]
  );

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
  };

  const handleAnalyze = async () => {
    if (!targetRole.trim()) {
      setError("Please enter a target role.");
      return;
    }
    setError(null);
    setStep("analyzing");

    // Animate progress steps
    let step = 0;
    const interval = setInterval(() => {
      step++;
      setProgressStep(step);
      setAnalyzeProgress(Math.min((step / analyzeSteps.length) * 90, 90));
      if (step >= analyzeSteps.length) clearInterval(interval);
    }, 500);

    try {
      const result: FullAnalysisResponse = await apiClient.analyzeResume(
        extractedText,
        targetRole.trim(),
        jobDescription.trim() || undefined
      );
      clearInterval(interval);
      setAnalyzeProgress(100);

      // Store result and navigate to results page
      sessionStorage.setItem("analysisResult", JSON.stringify(result));
      sessionStorage.setItem("targetRole", targetRole.trim());
      router.push("/results");
    } catch (err: unknown) {
      clearInterval(interval);
      setStep("configure");
      setError(err instanceof Error ? err.message : "Analysis failed. Please try again.");
    }
  };

  return (
    <main className="min-h-screen py-12">
      {/* Header */}
      <div className="max-w-3xl mx-auto px-6 mb-10">
        <Link
          href="/"
          className="inline-flex items-center gap-2 text-sm text-gray-500 hover:text-gray-300 transition-colors mb-8"
        >
          ← Back to home
        </Link>
        <h1 className="text-4xl font-bold mb-3">
          Analyze Your <span className="gradient-text">Resume</span>
        </h1>
        <p className="text-gray-400">
          Upload your resume and specify your target role. The AI pipeline handles the rest.
        </p>
      </div>

      <div className="max-w-3xl mx-auto px-6">
        {/* Step 1: Upload */}
        {step === "upload" && (
          <div className="animate-fade-up">
            <div
              id="resume-dropzone"
              className={`glass-card p-12 text-center cursor-pointer transition-all duration-200 ${
                dragOver
                  ? "border-violet-500/60 bg-violet-500/10"
                  : "hover:border-violet-500/30 hover:bg-white/[0.07]"
              }`}
              onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
              onDragLeave={() => setDragOver(false)}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <input
                ref={fileInputRef}
                type="file"
                id="resume-file-input"
                accept=".pdf,.docx,.doc,.txt"
                className="hidden"
                onChange={handleFileInput}
              />

              {uploading ? (
                <div className="space-y-4">
                  <div className="text-4xl animate-bounce">⏳</div>
                  <p className="text-gray-400">Uploading and extracting text…</p>
                </div>
              ) : (
                <>
                  <div className="text-5xl mb-5">📄</div>
                  <h2 className="text-xl font-semibold mb-3">
                    Drop your resume here
                  </h2>
                  <p className="text-gray-500 text-sm mb-6">
                    or click to browse — PDF, DOCX, or TXT up to 10 MB
                  </p>
                  <div className="inline-flex items-center gap-3 text-xs text-gray-600">
                    <span className="px-2 py-1 rounded bg-white/5 border border-white/10">PDF</span>
                    <span className="px-2 py-1 rounded bg-white/5 border border-white/10">DOCX</span>
                    <span className="px-2 py-1 rounded bg-white/5 border border-white/10">TXT</span>
                  </div>
                </>
              )}
            </div>

            {error && (
              <div className="mt-4 p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-sm">
                ⚠️ {error}
              </div>
            )}

            <p className="mt-6 text-center text-xs text-gray-600">
              🔒 Your resume is processed in-memory only. It is never stored or logged.
            </p>
          </div>
        )}

        {/* Step 2: Configure */}
        {step === "configure" && (
          <div className="animate-fade-up space-y-6">
            {/* File card */}
            <div className="glass-card p-5 flex items-center gap-4">
              <div className="text-3xl">✅</div>
              <div className="flex-1 min-w-0">
                <p className="font-medium truncate">{uploadedFile?.name}</p>
                <p className="text-sm text-gray-500">
                  {uploadedFile ? formatBytes(uploadedFile.size) : ""} · {wordCount} words extracted
                </p>
              </div>
              <button
                onClick={() => { setStep("upload"); setUploadedFile(null); setExtractedText(""); }}
                className="text-xs text-gray-500 hover:text-gray-300 transition-colors border border-white/10 rounded-lg px-3 py-1.5"
              >
                Change
              </button>
            </div>

            {/* Target Role */}
            <div className="glass-card p-6 space-y-4">
              <h2 className="font-semibold text-lg">Target Role *</h2>
              <input
                id="target-role-input"
                type="text"
                placeholder="e.g. Senior AI / ML Engineer"
                value={targetRole}
                onChange={(e) => setTargetRole(e.target.value)}
                className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-violet-500/60 focus:bg-white/[0.07] transition-all"
              />
              <div className="flex flex-wrap gap-2">
                {POPULAR_ROLES.map((role) => (
                  <button
                    key={role}
                    onClick={() => setTargetRole(role)}
                    className={`px-3 py-1.5 rounded-lg text-xs border transition-all ${
                      targetRole === role
                        ? "border-violet-500/60 bg-violet-500/20 text-violet-300"
                        : "border-white/10 text-gray-500 hover:text-gray-300 hover:border-white/20"
                    }`}
                  >
                    {role}
                  </button>
                ))}
              </div>
            </div>

            {/* Job Description (Optional) */}
            <div className="glass-card p-6 space-y-4">
              <div>
                <h2 className="font-semibold text-lg">Job Description <span className="text-gray-500 font-normal text-sm">(optional but recommended)</span></h2>
                <p className="text-xs text-gray-500 mt-1">
                  Paste the full job description to get detailed skill gap analysis and job match scoring.
                </p>
              </div>
              <textarea
                id="job-description-input"
                rows={8}
                placeholder="Paste the job description here…"
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-violet-500/60 focus:bg-white/[0.07] transition-all resize-none text-sm"
              />
            </div>

            {error && (
              <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-sm">
                ⚠️ {error}
              </div>
            )}

            <button
              id="analyze-button"
              onClick={handleAnalyze}
              disabled={!targetRole.trim()}
              className="btn-primary w-full !py-4 !text-base justify-center"
            >
              Run Intelligence Analysis →
            </button>
          </div>
        )}

        {/* Step 3: Analyzing */}
        {step === "analyzing" && (
          <div className="animate-fade-up">
            <div className="glass-card p-12 text-center space-y-8">
              {/* Progress ring */}
              <div className="relative inline-block">
                <svg width="120" height="120" className="-rotate-90">
                  <circle cx="60" cy="60" r="48" className="score-ring-track" />
                  <circle
                    cx="60"
                    cy="60"
                    r="48"
                    className="score-ring-fill stroke-violet-500"
                    strokeDasharray={`${2 * Math.PI * 48}`}
                    strokeDashoffset={`${2 * Math.PI * 48 * (1 - analyzeProgress / 100)}`}
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-2xl font-bold text-violet-400">{Math.round(analyzeProgress)}%</span>
                </div>
              </div>

              <div>
                <h2 className="text-xl font-semibold mb-2">Analyzing Your Resume</h2>
                <p className="text-sm text-gray-400 min-h-5 transition-all">
                  {analyzeSteps[Math.min(progressStep, analyzeSteps.length - 1)]}
                </p>
              </div>

              {/* Steps list */}
              <div className="text-left space-y-2 max-w-xs mx-auto">
                {analyzeSteps.map((s, i) => (
                  <div key={i} className={`flex items-center gap-3 text-sm transition-all ${
                    i < progressStep ? "text-emerald-400" : i === progressStep ? "text-violet-400" : "text-gray-700"
                  }`}>
                    <span>{i < progressStep ? "✓" : i === progressStep ? "⟳" : "○"}</span>
                    <span>{s}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
