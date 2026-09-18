import { proxyResponse, serviceFetch } from "@/lib/services";

export async function GET(request: Request) {
  const authorization = request.headers.get("authorization");
  return proxyResponse(
    await serviceFetch("auth", "/auth/me", {
      headers: authorization ? { authorization } : undefined,
    }),
  );
}
