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
  const [clear, setClear] = useState(false);

  async function handleSubmit() {
    setLoading(true);
    const urlList = urls.split("\n").filter(Boolean);
    try {
      const res = await crawlUrls(urlList, clear);
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

      <div className="mt-4 flex items-center justify-between">
        <label className="flex items-center text-sm text-zinc-400 cursor-pointer">
          <input
            type="checkbox"
            checked={clear}
            onChange={(e) => setClear(e.target.checked)}
            className="mr-2 rounded border-zinc-700 bg-zinc-800 text-blue-600 focus:ring-blue-500"
          />
          Clear database before crawling
        </label>

        <button
          onClick={handleSubmit}
          disabled={loading}
          className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded disabled:opacity-50 transition-colors"
        >
          {loading ? "Crawling..." : "Crawl & Store"}
        </button>
      </div>

      {result && (
        <p className="mt-3 text-green-400 text-sm">
          {clear ? "Database cleared and " : ""}Stored {result.chunks} chunks successfully
        </p>
      )}
    </div>
  );
}
