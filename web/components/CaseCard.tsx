import Link from "next/link";

export type CaseSummary = {
  id: string;
  title: string;
  summary: string;
  status: string;
  created_at?: string;
};

export function CaseCard({ item }: { item: CaseSummary }) {
  return (
    <article className="card">
      <div className="cardHeader">
        <span className={`status status-${item.status}`}>{item.status}</span>
        <span className="muted">{item.id.slice(0, 8)}</span>
      </div>
      <h2>{item.title}</h2>
      <p>{item.summary}</p>
      <Link href={`/cases/${item.id}`}>Open case →</Link>
    </article>
  );
}
