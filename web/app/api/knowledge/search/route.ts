import { proxyResponse, serviceFetch } from "@/lib/services";

export async function GET(request: Request) {
  const query = new URL(request.url).searchParams.get("q") ?? "";
  return proxyResponse(
    await serviceFetch("knowledge", `/search?q=${encodeURIComponent(query)}`),
  );
}
