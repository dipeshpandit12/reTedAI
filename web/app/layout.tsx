import Link from "next/link";
import "./globals.css";

export const metadata = {
  title: "reTedAI",
  description: "AI-assisted case diagnosis and automation",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <header className="siteHeader">
          <Link className="brand" href="/">reTedAI</Link>
          <nav aria-label="Primary navigation">
            <Link href="/">Cases</Link>
            <Link href="/cases/new">New case</Link>
            <Link href="/knowledge">Knowledge</Link>
          </nav>
        </header>
        <main>{children}</main>
      </body>
    </html>
  );
}
