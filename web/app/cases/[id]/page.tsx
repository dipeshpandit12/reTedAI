import { DiagnosisPanel } from "@/components/DiagnosisPanel";
import { Timeline, type TimelineEvent } from "@/components/Timeline";
import { serviceFetch } from "@/lib/services";
import { notFound } from "next/navigation";

type CaseDetail = { id: string; title: string; summary: string; status: string; diagnosis?: string | null; actions: TimelineEvent[] };

export default async function CaseDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  let item: CaseDetail;
  try {
    const response = await serviceFetch("case", `/cases/${id}`);
    if (response.status === 404) notFound();
    if (!response.ok) throw new Error("case service error");
    item = await response.json();
  } catch {
    notFound();
  }

  return (
    <>
      <div className="pageHeading"><div><p className="eyebrow">Case {item.id.slice(0, 8)}</p><h1>{item.title}</h1><p>{item.summary}</p></div></div>
      <div className="detailGrid"><DiagnosisPanel caseId={item.id} diagnosis={item.diagnosis} /><Timeline events={item.actions ?? []} /></div>
    </>
  );
}
