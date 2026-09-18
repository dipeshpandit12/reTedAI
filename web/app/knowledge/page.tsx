"use client";

import { type FormEvent, useState } from "react";

type Result = { id: string; title: string; content: string; score: number };

export default function KnowledgePage() {
  const [results, setResults] = useState<Result[]>([]);
  const [searched, setSearched] = useState(false);

  async function search(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const query = new FormData(event.currentTarget).get("query");
    const response = await fetch(`/api/knowledge/search?q=${encodeURIComponent(String(query))}`);
    setResults(response.ok ? await response.json() : []);
    setSearched(true);
  }

  return (
    <>
      <div className="pageHeading"><div><p className="eyebrow">Retrieval</p><h1>Knowledge search</h1></div></div>
      <form className="search" onSubmit={search}><input name="query" aria-label="Search query" placeholder="Search past cases and runbooks" required /><button type="submit">Search</button></form>
      <section className="grid">{results.map((result) => <article className="card" key={result.id}><span className="muted">Score {result.score.toFixed(2)}</span><h2>{result.title}</h2><p>{result.content}</p></article>)}</section>
      {searched && results.length === 0 && <p className="empty">No matching knowledge found.</p>}
    </>
  );
}
