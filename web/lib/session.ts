export type Session = {
  user: { id: string; name: string; role: "analyst" | "approver" | "admin" };
};

export async function getSession(): Promise<Session> {
  // Keycloak seam: replace this deterministic development identity with
  // verified claims from the Keycloak access token.
  return {
    user: { id: "demo-user", name: "Demo Analyst", role: "approver" },
  };
}

export function sessionHeaders(session: Session): HeadersInit {
  return {
    "x-user-id": session.user.id,
    "x-user-role": session.user.role,
  };
}
