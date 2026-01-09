"use client";

import { useState } from "react";
import { askQuestion } from "@/lib/api";

interface ChatBoxProps {
  question: string;
  setQuestion: (question: string) => void;
  answer: string;
  setAnswer: (answer: string) => void;
}

export default function ChatBox({ question, setQuestion, answer, setAnswer }: ChatBoxProps) {
  const [loading, setLoading] = useState(false);
  const [sources, setSources] = useState<string[]>([]);
  const [error, setError] = useState("");

  async function handleAsk() {
    if (!question.trim()) return;
    setLoading(true);
    setError("");
    setAnswer("");
    setSources([]);
    try {
      console.log("DEBUG: Sending question to API:", question);
      const res = await askQuestion(question);
      console.log("DEBUG: Received response:", res);
      
      if (res.answer) {
        setAnswer(res.answer);
        setSources(res.sources || []);
      } else {
        setError("AI returned an empty answer. Try another question.");
      }
    } catch (e: any) {
      console.error("DEBUG: ChatBox Error:", e);
      setError(`Failed to get answer: ${e.message || "Unknown error"}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="bg-zinc-900 p-6 rounded-xl shadow-md mt-8 border border-zinc-800">
      <h2 className="text-xl font-semibold mb-4 text-green-400">Knowledge Assistant</h2>

      <div className="flex gap-2">
        <input
          className="flex-grow p-3 rounded bg-white text-black border border-zinc-300 focus:border-green-500 outline-none transition-colors placeholder:text-zinc-500"
          placeholder="Ask something about the processed websites..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleAsk()}
        />
        <button
          onClick={handleAsk}
          disabled={loading}
          className="bg-green-600 hover:bg-green-700 px-6 py-2 rounded-lg font-medium disabled:opacity-50 transition-all flex items-center gap-2"
        >
          {loading ? (
            <>
              <span className="animate-spin text-lg">◌</span>
              Thinking...
            </>
          ) : "Ask"}
        </button>
      </div>

      {error && (
        <div className="mt-4 p-4 bg-red-900/30 border border-red-500/50 rounded text-red-200 text-sm">
          {error}
        </div>
      )}

      {answer && (
        <div className="mt-6 space-y-4 animate-in fade-in duration-500">
          <div className="p-5 bg-zinc-800/50 border border-zinc-700 rounded-lg">
            <h3 className="text-xs font-bold uppercase tracking-wider text-zinc-500 mb-2">Answer</h3>
            <div className="text-zinc-200 whitespace-pre-wrap leading-relaxed">
              {answer}
            </div>
          </div>

          {sources.length > 0 && (
            <div className="p-4 bg-zinc-900/50 border border-zinc-800 rounded-lg">
              <h3 className="text-xs font-bold uppercase tracking-wider text-zinc-500 mb-2">Sources</h3>
              <ul className="text-xs text-zinc-400 space-y-1 mt-2">
                {sources.map((src, i) => (
                  <li key={i} className="truncate hover:text-green-400 cursor-default transition-colors">
                    • {src}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
