"use client";

import { useState, useEffect } from "react";
import UrlForm from "@/components/UrlForm";
import ChatBox from "@/components/ChatBox";

export default function Home() {
  const [urls, setUrls] = useState("");
  const [crawlResult, setCrawlResult] = useState<any>(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [isClient, setIsClient] = useState(false);

  // Load from LocalStorage on mount
  useEffect(() => {
    setIsClient(true);
    const savedUrls = localStorage.getItem("urls");
    const savedResult = localStorage.getItem("crawlResult");
    const savedQuestion = localStorage.getItem("question");
    const savedAnswer = localStorage.getItem("answer");

    if (savedUrls) setUrls(savedUrls);
    if (savedResult) setCrawlResult(JSON.parse(savedResult));
    if (savedQuestion) setQuestion(savedQuestion);
    if (savedAnswer) setAnswer(savedAnswer);
  }, []);

  // Save to LocalStorage on change
  useEffect(() => {
    if (!isClient) return;
    localStorage.setItem("urls", urls);
  }, [urls, isClient]);

  useEffect(() => {
    if (!isClient) return;
    if (crawlResult) {
      localStorage.setItem("crawlResult", JSON.stringify(crawlResult));
    } else {
      localStorage.removeItem("crawlResult");
    }
  }, [crawlResult, isClient]);

  useEffect(() => {
    if (!isClient) return;
    localStorage.setItem("question", question);
  }, [question, isClient]);

  useEffect(() => {
    if (!isClient) return;
    localStorage.setItem("answer", answer);
  }, [answer, isClient]);

  const handleReset = () => {
    if (confirm("Are you sure you want to reset all data?")) {
      setUrls("");
      setCrawlResult(null);
      setQuestion("");
      setAnswer("");
      localStorage.clear();
    }
  };

  if (!isClient) return <div className="min-h-screen bg-black text-white p-10">Loading...</div>;

  return (
    <main className="min-h-screen bg-black text-white p-10">
      <div className="flex justify-between items-center mb-8 max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold text-center flex-grow">
          WebCrawlRAG
        </h1>
        <button
          onClick={handleReset}
          className="bg-red-600 hover:bg-red-700 px-3 py-1 rounded text-sm text-white"
        >
          Reset
        </button>
      </div>

      <div className="max-w-3xl mx-auto">
        <UrlForm
          urls={urls}
          setUrls={setUrls}
          result={crawlResult}
          setResult={setCrawlResult}
        />
        <ChatBox
          question={question}
          setQuestion={setQuestion}
          answer={answer}
          setAnswer={setAnswer}
        />
      </div>
    </main>
  );
}
