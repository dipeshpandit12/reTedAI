import { CaseCard, type CaseSummary } from "@/components/CaseCard";
import { serviceFetch } from "@/lib/services";

export const dynamic = "force-dynamic";

async function getCases(): Promise<CaseSummary[]> {
  try {
    const response = await serviceFetch("case", "/cases");
    if (!response.ok) return [];
    return response.json();
  } catch {
    return [];
  }
}

export default async function CasesPage() {
  const cases = await getCases();
  return (
    <>
      <div className="pageHeading">
        <div><p className="eyebrow">Operations workspace</p><h1>Cases</h1></div>
        <a className="button" href="/cases/new">Create case</a>
      </div>
      <section className="grid" aria-label="Case list">
        {cases.length > 0 ? cases.map((item) => <CaseCard key={item.id} item={item} />) : (
          <div className="empty"><h2>No cases yet</h2><p>Create the first case or load the seed data.</p></div>
        )}
      </section>
    </>
  );
}
