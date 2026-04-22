import { useState } from 'react';

export default function D360Modal({ isOpen, onClose, reportData }) {
  const [apiKey, setApiKey] = useState('');
  const [projectSlug, setProjectSlug] = useState('');
  const [status, setStatus] = useState('idle'); // idle, loading, success, error
  const [errorMsg, setErrorMsg] = useState('');

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!apiKey || !projectSlug) return;

    setStatus('loading');
    setErrorMsg('');

    try {
      const response = await fetch('/api/export/document360', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          report: reportData,
          api_key: apiKey,
          project_slug: projectSlug,
        }),
      });

      if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail || err.error || `Export failed (${response.status})`);
      }

      setStatus('success');
      setTimeout(() => { onClose(); setStatus('idle'); }, 2000);
    } catch (err) {
      setStatus('error');
      setErrorMsg(err.message);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black/40 backdrop-blur-sm" onClick={onClose} />

      {/* Modal */}
      <div className="relative glass-panel bg-[#0A0118]/90 rounded-2xl shadow-[0_0_40px_rgba(0,0,0,0.5)] border border-white/20 w-full max-w-md animate-fade-in">
        <div className="p-6">
          <div className="flex items-center justify-between mb-5">
            <div>
              <h2 className="text-lg font-semibold text-white">Push to Document360</h2>
              <p className="text-xs text-white/60 mt-0.5">Enter your Document360 credentials</p>
            </div>
            <button onClick={onClose} className="text-white/40 hover:text-white p-1 transition-colors">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-medium text-white/80 mb-1.5">API Key</label>
              <input
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="Enter your Document360 API key"
                className="w-full text-sm bg-white/5 border border-white/10 text-white placeholder-white/30 rounded-lg px-3 py-2.5 focus:outline-none focus:bg-white/10 focus:border-primary-light/50 transition-colors"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-white/80 mb-1.5">Project Slug</label>
              <input
                type="text"
                value={projectSlug}
                onChange={(e) => setProjectSlug(e.target.value)}
                placeholder="e.g., my-docs-project"
                className="w-full text-sm bg-white/5 border border-white/10 text-white placeholder-white/30 rounded-lg px-3 py-2.5 focus:outline-none focus:bg-white/10 focus:border-primary-light/50 transition-colors font-mono"
                required
              />
            </div>

            {status === 'error' && (
              <div className="p-3 bg-danger/20 rounded-lg border border-danger/30 text-red-300 text-xs shadow-[0_0_10px_rgba(239,68,68,0.2)]">
                {errorMsg}
              </div>
            )}

            {status === 'success' && (
              <div className="p-3 bg-success/20 rounded-lg border border-success/30 text-green-300 text-xs flex items-center gap-2 shadow-[0_0_10px_rgba(16,185,129,0.2)]">
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                </svg>
                Successfully pushed to Document360!
              </div>
            )}

            <button
              type="submit"
              disabled={status === 'loading' || status === 'success'}
              className={`w-full py-2.5 rounded-xl text-[15px] tracking-wide font-semibold transition-all duration-300
                ${status === 'loading' ? 'bg-primary/50 text-white cursor-wait' :
                  status === 'success' ? 'bg-success/80 text-white shadow-[0_0_15px_rgba(16,185,129,0.5)]' :
                  'glow-button text-white hover:-translate-y-0.5'}`}
            >
              {status === 'loading' ? 'Pushing...' :
               status === 'success' ? 'Done!' :
               'Push to Document360'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
