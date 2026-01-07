import UrlForm from "@/components/UrlForm";
import ChatBox from "@/components/ChatBox";

export default function Home() {
  return (
    <main className="min-h-screen bg-black text-white p-10">
      <h1 className="text-3xl font-bold mb-8 text-center">
        WebCrawlRAG
      </h1>

      <div className="max-w-3xl mx-auto">
        <UrlForm />
        <ChatBox />
      </div>
    </main>
  );
}
