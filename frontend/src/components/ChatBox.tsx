"use client";

import { useState } from "react";
import { askQuestion } from "@/lib/api";

export default function ChatBox() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleAsk() {
    setLoading(true);
    const res = await askQuestion(question);
    setAnswer(res.answer);
    setLoading(false);
  }

  return (
    <div className="bg-zinc-900 p-6 rounded-xl shadow-md mt-8">
      <h2 className="text-xl font-semibold mb-4">Ask a Question</h2>

      <input
        className="w-full p-3 rounded bg-zinc-800 text-white"
        placeholder="Ask something about the website..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button
        onClick={handleAsk}
        className="mt-4 bg-green-600 hover:bg-green-700 px-4 py-2 rounded"
      >
        {loading ? "Thinking..." : "Ask"}
      </button>

      {answer && (
        <div className="mt-4 p-4 bg-zinc-800 rounded">
          <pre className="text-gray-200 whitespace-pre-wrap leading-relaxed">
  {answer}
</pre>

        </div>
      )}
    </div>
  );
}
