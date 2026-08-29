import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Resume Intelligence Analyzer — AI-Powered Career Insights",
  description:
    "Upload your resume, compare it against a target role, identify skill gaps, and receive actionable AI-powered recommendations. Powered by NLP, semantic matching, and LLM reasoning.",
  keywords: [
    "resume analyzer",
    "AI resume review",
    "job match score",
    "skill gap analysis",
    "ATS compatibility",
    "career intelligence",
  ],
  authors: [{ name: "rknaga31" }],
  openGraph: {
    title: "Resume Intelligence Analyzer",
    description: "AI-powered resume analysis and career intelligence platform.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="font-sans antialiased bg-gray-950 text-gray-100 min-h-screen">
        {children}
      </body>
    </html>
  );
}
