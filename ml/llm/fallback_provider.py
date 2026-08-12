"""
Rule-based fallback LLM provider — Milestone 10.

Used when no external LLM API key is configured.
Produces deterministic, structured output based on scoring results.
Never claims to be an LLM response.
"""
from __future__ import annotations

from ml.llm.base import BaseLLMProvider, LLMAnalysisOutput


class FallbackProvider(BaseLLMProvider):
    """Deterministic rule-based provider used when no LLM is configured."""

    provider_name = "fallback"

    def synthesize(
        self,
        resume_text: str,
        target_role: str,
        skill_match: dict,
        ats_issues: list[str],
        achievement_issues: list[str],
    ) -> LLMAnalysisOutput:
        """Generate structured analysis without an external LLM.

        Args:
            resume_text: Resume text (not used by fallback — not stored or logged).
            target_role: Target job role.
            skill_match: Matched/partial/missing skill breakdown.
            ats_issues: ATS compatibility issues detected.
            achievement_issues: Bullet improvement suggestions.

        Returns:
            LLMAnalysisOutput with deterministic content.
        """
        matched = skill_match.get("matched", [])
        missing = skill_match.get("missing", [])
        partial = skill_match.get("partial", [])

        strengths: list[str] = []
        weaknesses: list[str] = []
        recommendations: list[str] = []
        roadmap: list[str] = []

        # Strengths from skill matches
        if matched:
            strengths.append(
                f"Strong technical skill alignment: {', '.join(matched[:5])} are directly matched to the {target_role} role."
            )
        if partial:
            partial_pairs = [f"{p['resume_skill']} (related to {p['job_skill']})" for p in partial[:3]]
            strengths.append(f"Related skill evidence found: {'; '.join(partial_pairs)}.")

        # Weaknesses from missing skills + ATS issues
        if missing:
            weaknesses.append(
                f"Missing required skills for {target_role}: {', '.join(missing[:5])}."
            )
        for issue in ats_issues[:3]:
            weaknesses.append(issue)

        # Recommendations
        for skill in missing[:3]:
            recommendations.append(
                f"Build evidence of '{skill}': add a project, certification, or contribution that demonstrates this skill."
            )
        for suggestion in achievement_issues[:2]:
            recommendations.append(suggestion)
        if not recommendations:
            recommendations.append(
                "Continue building depth in your primary technical stack and quantify accomplishments with specific metrics."
            )

        # Career roadmap
        if missing:
            roadmap.append(f"Step 1: Address the highest-priority skill gaps: {', '.join(missing[:3])}.")
            roadmap.append("Step 2: Quantify your existing experience bullets with concrete metrics (%, scale, time).")
            roadmap.append(f"Step 3: Build and publish 1-2 portfolio projects demonstrating skills relevant to {target_role}.")
        else:
            roadmap.append("Step 1: Quantify all experience bullets with concrete metrics.")
            roadmap.append("Step 2: Strengthen the Summary section to target the specific role.")
            roadmap.append(f"Step 3: Tailor the resume keywords for '{target_role}' positions.")

        summary_parts = []
        if matched:
            summary_parts.append(f"demonstrates solid alignment in {', '.join(matched[:3])}")
        if missing:
            summary_parts.append(f"has skill gaps in {', '.join(missing[:3])}")
        summary = (
            f"Your resume {' and '.join(summary_parts)} for the {target_role} role. "
            f"Focus on the recommended improvements below to strengthen your application."
            if summary_parts
            else f"Your resume has been analyzed for the {target_role} role. Review the recommendations below."
        )

        return LLMAnalysisOutput(
            executive_summary=summary,
            strengths=strengths or ["Resume has been processed. Configure an LLM provider for AI-powered narrative analysis."],
            weaknesses=weaknesses or ["No major structural issues detected."],
            actionable_recommendations=recommendations,
            career_roadmap=roadmap,
            provider_used=self.provider_name,
        )
