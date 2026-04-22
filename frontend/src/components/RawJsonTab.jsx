import { useState } from 'react';
import { copyToClipboard } from '../utils';

export default function RawJsonTab({ data }) {
  const [copied, setCopied] = useState(false);
  const [collapsed, setCollapsed] = useState({});

  const jsonString = JSON.stringify(data, null, 2);

  const handleCopy = () => {
    copyToClipboard(jsonString);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-4 animate-fade-in">
      <div className="flex items-center justify-between">
        <h3 className="text-[15px] font-semibold text-white tracking-wide">Full API Response</h3>
        <button
          onClick={handleCopy}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[13px] font-medium transition-all
            ${copied ? 'bg-success/20 text-success border border-success/30' : 'bg-white/10 border border-white/10 text-white/80 hover:bg-white/20 hover:text-white'}`}
        >
          {copied ? (
            <>
              <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
              </svg>
              Copied!
            </>
          ) : (
            <>
              <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              Copy to clipboard
            </>
          )}
        </button>
      </div>

      <div className="glass-panel p-0 bg-black/40 rounded-xl overflow-hidden shadow-lg border border-white/10">
        <div className="p-4 overflow-x-auto max-h-[600px] overflow-y-auto">
          <pre className="text-[13px] leading-relaxed font-mono">
            <JsonHighlighter json={jsonString} />
          </pre>
        </div>
      </div>
    </div>
  );
}

function JsonHighlighter({ json }) {
  const highlighted = json.replace(
    /("(?:\\.|[^"\\])*")\s*:/g,
    '<span style="color:#89b4fa">$1</span>:'
  ).replace(
    /:\s*("(?:\\.|[^"\\])*")/g,
    ': <span style="color:#a6e3a1">$1</span>'
  ).replace(
    /:\s*(\d+\.?\d*)/g,
    ': <span style="color:#fab387">$1</span>'
  ).replace(
    /:\s*(true|false)/g,
    ': <span style="color:#cba6f7">$1</span>'
  ).replace(
    /:\s*(null)/g,
    ': <span style="color:#6c7086">$1</span>'
  );

  return <code dangerouslySetInnerHTML={{ __html: highlighted }} className="text-[#cdd6f4]" />;
}
