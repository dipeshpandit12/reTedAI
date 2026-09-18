"use client";

import { useState } from "react";

export function DiagnosisPanel({
  caseId,
  diagnosis,
}: {
  caseId: string;
  diagnosis?: string | null;
}) {
  const [status, setStatus] = useState("pending");
  const [message, setMessage] = useState("");

  async function approve() {
    setMessage("Approving…");
    const response = await fetch(`/api/cases/${caseId}/approve`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ note: "Approved from case detail" }),
    });
    if (!response.ok) {
      setMessage("Approval failed. Check the case service.");
      return;
    }
    setStatus("approved");
    setMessage("Diagnosis approved.");
  }

  return (
    <section className="panel">
      <div className="cardHeader">
        <h2>AI diagnosis</h2>
        <span className={`status status-${status}`}>{status}</span>
      </div>
      <p>{diagnosis ?? "No diagnosis has been generated yet."}</p>
      <button onClick={approve} type="button" disabled={status === "approved"}>
        Approve diagnosis
      </button>
      {message && <p className="muted" role="status">{message}</p>}
    </section>
  );
}
