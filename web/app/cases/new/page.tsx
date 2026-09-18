"use client";

import { useRouter } from "next/navigation";
import { type FormEvent, useState } from "react";

export default function NewCasePage() {
  const router = useRouter();
  const [error, setError] = useState("");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const response = await fetch("/api/cases", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ title: form.get("title"), summary: form.get("summary") }),
    });
    if (!response.ok) {
      setError("Could not create the case.");
      return;
    }
    const created = await response.json();
    router.push(`/cases/${created.id}`);
  }

  return (
    <section className="formPage">
      <p className="eyebrow">New investigation</p><h1>Create a case</h1>
      <form onSubmit={submit}>
        <label>Title<input name="title" required minLength={3} /></label>
        <label>Summary<textarea name="summary" required minLength={10} rows={7} /></label>
        <button type="submit">Create case</button>
        {error && <p className="error" role="alert">{error}</p>}
      </form>
    </section>
  );
}
