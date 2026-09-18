import { proxyResponse, serviceFetch } from "@/lib/services";

export async function DELETE(request: Request) {
  const authorization = request.headers.get("authorization");
  return proxyResponse(
    await serviceFetch("auth", "/auth/session", {
      method: "DELETE",
      headers: authorization ? { authorization } : undefined,
    }),
  );
}
