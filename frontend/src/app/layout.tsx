import "./globals.css";

export const metadata = {
  title: "WebCrawlRAG",
  description: "RAG-based Web Crawling Assistant",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-black text-white">
        {children}
      </body>
    </html>
  );
}
