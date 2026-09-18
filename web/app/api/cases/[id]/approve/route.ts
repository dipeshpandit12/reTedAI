import { getSession, sessionHeaders } from "@/lib/session";
import { proxyResponse, serviceFetch } from "@/lib/services";

type Context = { params: Promise<{ id: string }> };

export async function POST(request: Request, { params }: Context) {
  const { id } = await params;
  const session = await getSession();
  return proxyResponse(
    await serviceFetch("case", `/cases/${id}/approve`, {
      method: "POST",
      headers: sessionHeaders(session),
      body: await request.text(),
    }),
  );
}
