import React from "react";

function Result({ result }) {
  if (!result) return null;

  if (result === "loading") {
    return (
      <div className="pipeline-container animate-fade-in" style={{ textAlign: "center", padding: "30px" }}>
        <div className="spinner" style={{ fontSize: "1.8rem", marginBottom: "10px" }}>🔍</div>
        <p>Analyzing and crawling web content...</p>
      </div>
    );
  }

  // Support both new search-agent response keys and old user_friendly keys
  const synthesizedAnswer = result.synthesized_answer || result.user_friendly?.summary;
  const keyPoints = result.key_points || [];
  const actionPrompt = result.action_prompt || result.recommendation;
  const jobs = result.jobs || [];
  const sources = result.sources || [];
  const intent = result.intent || (result.user_friendly?.key_claim_verdict?.toLowerCase() === "jobs" ? "jobs" : "general");
  
  const confidenceScore = result.combined_score || result.user_friendly?.confidence_score || "100%";
  const confidenceLevel = result.user_friendly?.confidence_level || "medium";

  return (
    <div className="result-container animate-fade-in">
      {/* Intent / Status Badge */}
      <div className="result-header">
        <span className="badge badge-intent">
          Intent: {intent ? intent.toUpperCase() : "GENERAL Q&A"}
        </span>
        <span className={`badge badge-conf-${confidenceLevel}`}>
          Match confidence: {confidenceScore}
        </span>
      </div>

      {/* Main Synthesized Answer */}
      {synthesizedAnswer && (
        <div className="answer-section">
          <h4>🧠 Synthesized Answer</h4>
          <p className="main-answer-text">{synthesizedAnswer}</p>
        </div>
      )}

      {/* Key Takeaways */}
      {keyPoints.length > 0 && (
        <div className="key-points-section">
          <h5>📌 Key Highlights</h5>
          <ul className="key-points-list">
            {keyPoints.map((point, index) => (
              <li key={index}>{point}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Action-Oriented Guidance */}
      {actionPrompt && (
        <div className="action-guidance-card">
          <div className="action-guidance-icon">💡</div>
          <div className="action-guidance-body">
            <h6>Recommended Action</h6>
            <p>{actionPrompt}</p>
          </div>
        </div>
      )}

      {/* Jobs Grid (if job intent) */}
      {intent === "jobs" && jobs.length > 0 && (
        <div className="jobs-section animate-fade-in">
          <h5>💼 Matching Openings Found</h5>
          <div className="jobs-grid">
            {jobs.map((job, idx) => (
              <div key={idx} className="job-card">
                <div className="job-card-header">
                  <span className="job-match-badge" style={{
                    background: job.match_score >= 90 ? "rgba(16, 185, 129, 0.15)" : "rgba(59, 130, 246, 0.15)",
                    color: job.match_score >= 90 ? "#10b981" : "#3b82f6",
                    border: job.match_score >= 90 ? "1px solid rgba(16, 185, 129, 0.3)" : "1px solid rgba(59, 130, 246, 0.3)"
                  }}>
                    {job.match_score}% Match
                  </span>
                </div>
                <h6 className="job-title">{job.title}</h6>
                <div className="job-company">{job.company}</div>
                <div className="job-details">
                  <span>📍 {job.location}</span>
                  {job.salary_range && job.salary_range !== "Not specified" && (
                    <span>💵 {job.salary_range}</span>
                  )}
                </div>
                <a
                  href={job.apply_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-apply"
                >
                  Apply Now 🚀
                </a>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Cited Sources & References */}
      {sources.length > 0 && (
        <div className="sources-section">
          <h5>🔗 Cited Sources & References</h5>
          <div className="sources-list">
            {sources.map((source, idx) => (
              <div key={idx} className="source-card">
                <div className="source-card-header">
                  <span className="source-rank">#{source.rank || idx + 1}</span>
                  <a
                    href={source.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="source-title"
                  >
                    {source.title}
                  </a>
                </div>
                <p className="source-snippet">{source.snippet}</p>
                <div className="source-metadata">
                  <span className="source-domain">🌐 {source.domain}</span>
                  <span className="source-score">Relevance Match: {source.relevance_score}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default Result;