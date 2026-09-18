export type ServiceName = "auth" | "case" | "ai" | "knowledge" | "automation";

const serviceUrls: Record<ServiceName, string> = {
  auth: process.env.AUTH_SERVICE_URL ?? "http://localhost:8005",
  case: process.env.CASE_SERVICE_URL ?? "http://localhost:8001",
  ai: process.env.AI_SERVICE_URL ?? "http://localhost:8002",
  knowledge: process.env.KNOWLEDGE_SERVICE_URL ?? "http://localhost:8003",
  automation: process.env.AUTOMATION_SERVICE_URL ?? "http://localhost:8004",
};

export async function serviceFetch(
  service: ServiceName,
  path: string,
  init: RequestInit = {},
): Promise<Response> {
  const headers = new Headers(init.headers);
  if (init.body && !headers.has("content-type")) {
    headers.set("content-type", "application/json");
  }

  return fetch(`${serviceUrls[service]}${path}`, {
    ...init,
    headers,
    cache: "no-store",
  });
}

export async function proxyResponse(response: Response): Promise<Response> {
  const contentType = response.headers.get("content-type");
  const body = response.status === 204 || response.status === 304
    ? null
    : await response.arrayBuffer();
  return new Response(body, {
    status: response.status,
    headers: contentType ? { "content-type": contentType } : undefined,
  });
}
