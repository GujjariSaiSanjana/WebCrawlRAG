"use client";

import { useState } from "react";
import { crawlUrls } from "@/lib/api";

interface UrlFormProps {
  urls: string;
  setUrls: (urls: string) => void;
  result: any;
  setResult: (result: any) => void;
}

export default function UrlForm({ urls, setUrls, result, setResult }: UrlFormProps) {
  const [loading, setLoading] = useState(false);

  async function handleSubmit() {
    setLoading(true);
    const urlList = urls.split("\n").filter(Boolean);
    try {
      const res = await crawlUrls(urlList);
      setResult(res);
    } catch (e) {
      console.error(e);
      alert("Error crawling URLs");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="bg-zinc-900 p-6 rounded-xl shadow-md">
      <h2 className="text-xl font-semibold mb-4">Submit Website URLs</h2>

      <textarea
        className="w-full p-3 rounded bg-zinc-800 text-white"
        rows={4}
        placeholder="Enter one URL per line"
        value={urls}
        onChange={(e) => setUrls(e.target.value)}
      />

      <button
        onClick={handleSubmit}
        disabled={loading}
        className="mt-4 bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded disabled:opacity-50"
      >
        {loading ? "Crawling..." : "Crawl & Store"}
      </button>

      {result && (
        <p className="mt-3 text-green-400">
          Stored {result.chunks} chunks successfully
        </p>
      )}
    </div>
  );
}
