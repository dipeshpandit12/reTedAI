import { getSession, sessionHeaders } from "@/lib/session";
import { proxyResponse, serviceFetch } from "@/lib/services";

export async function GET() {
  return proxyResponse(await serviceFetch("case", "/cases"));
}

export async function POST(request: Request) {
  const session = await getSession();
  return proxyResponse(
    await serviceFetch("case", "/cases", {
      method: "POST",
      headers: sessionHeaders(session),
      body: await request.text(),
    }),
  );
}
