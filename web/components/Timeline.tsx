export type TimelineEvent = {
  id: string;
  action: string;
  actor: string;
  created_at: string;
};

export function Timeline({ events }: { events: TimelineEvent[] }) {
  return (
    <section className="panel">
      <h2>Timeline</h2>
      {events.length === 0 ? (
        <p className="muted">No activity yet.</p>
      ) : (
        <ol className="timeline">
          {events.map((event) => (
            <li key={event.id}>
              <strong>{event.action}</strong>
              <span>{event.actor} · {new Date(event.created_at).toLocaleString()}</span>
            </li>
          ))}
        </ol>
      )}
    </section>
  );
}
