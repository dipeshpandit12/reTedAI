import { proxyResponse, serviceFetch } from "@/lib/services";

export async function POST(request: Request) {
  return proxyResponse(
    await serviceFetch("auth", "/auth/dev-token", {
      method: "POST",
      body: await request.text(),
    }),
  );
}
