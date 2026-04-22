import { useState, useRef, useCallback } from 'react';
import { formatFileSize } from '../utils';

const ACCEPTED_TYPES = ['.pdf', '.docx'];

export default function UploadScreen({ onAnalyze, isLoading, loadingStep }) {
  const [file, setFile] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const [error, setError] = useState('');
  const inputRef = useRef(null);

  const validateFile = useCallback((f) => {
    const ext = '.' + f.name.split('.').pop().toLowerCase();
    if (!ACCEPTED_TYPES.includes(ext)) {
      setError(`Unsupported file type: ${ext}. Only .pdf and .docx files are accepted.`);
      return false;
    }
    if (f.size > 50 * 1024 * 1024) {
      setError('File too large. Maximum size is 50 MB.');
      return false;
    }
    setError('');
    return true;
  }, []);

  const handleFile = useCallback((f) => {
    if (validateFile(f)) setFile(f);
  }, [validateFile]);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setDragOver(false);
    const f = e.dataTransfer.files?.[0];
    if (f) handleFile(f);
  }, [handleFile]);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setDragOver(true);
  }, []);

  const handleDragLeave = useCallback(() => setDragOver(false), []);

  const steps = [
    { key: 'parsing', label: 'Parsing document...' },
    { key: 'extracting', label: 'Extracting metrics...' },
    { key: 'analyzing', label: 'Running AI analysis...' },
  ];

  const currentStepIndex = steps.findIndex(s => s.key === loadingStep);

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-xl animate-fade-in">
        {/* Logo / brand - Centered styling matching the galaxy theme */}
        <div className="text-center mb-10">
          <h1 className="text-4xl lg:text-5xl font-bold font-display text-text-primary leading-tight tracking-tight mb-4">
            Flawless Migration.<br/>
          </h1>
          <p className="text-text-secondary mt-1.5 text-sm">
            Analyze your documents for migration readiness
          </p>
        </div>

        {/* Upload card (Glass Panel) */}
        <div className="glass-panel rounded-2xl p-8 relative overflow-hidden">
          {!isLoading ? (
            <>
              <div
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onClick={() => inputRef.current?.click()}
                className={`border border-dashed rounded-xl p-10 text-center cursor-pointer transition-all duration-300
                  ${dragOver ? 'border-primary-light bg-primary/10' : 'border-white/20 hover:border-primary-light/50 hover:bg-white/5'}
                `}
              >
                <input
                  ref={inputRef}
                  type="file"
                  accept=".pdf,.docx"
                  className="hidden"
                  onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
                />
                <div className="w-14 h-14 mx-auto mb-4 bg-primary/10 rounded-2xl flex items-center justify-center">
                  <svg className="w-7 h-7 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
                  </svg>
                </div>
                <p className="text-sm font-medium text-text-primary">
                  Drop your file here or <span className="text-primary-light underline underline-offset-4 decoration-primary-light/30">browse</span>
                </p>
                <p className="text-xs text-text-muted mt-2">
                  Supports .pdf and .docx (up to 50 MB)
                </p>
              </div>

              {/* Error */}
              {error && (
                <div className="mt-4 p-3 bg-danger-light rounded-lg border border-danger/20 text-danger text-sm flex items-center gap-2">
                  <svg className="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
                  </svg>
                  {error}
                </div>
              )}

              {/* File info */}
              {file && (
                <div className="mt-4 p-4 glass-panel bg-black/20 rounded-xl flex items-center justify-between">
                  <div className="flex items-center gap-3 min-w-0">
                    <div className={`w-10 h-10 rounded-lg flex items-center justify-center text-white text-xs font-bold ${file.name.endsWith('.pdf') ? 'bg-red-500' : 'bg-blue-500'}`}>
                      {file.name.split('.').pop().toUpperCase()}
                    </div>
                    <div className="min-w-0">
                      <p className="text-sm font-medium text-text-primary truncate">{file.name}</p>
                      <p className="text-xs text-text-muted">{formatFileSize(file.size)}</p>
                    </div>
                  </div>
                  <button
                    onClick={(e) => { e.stopPropagation(); setFile(null); setError(''); }}
                    className="text-text-muted hover:text-text-secondary p-1"
                  >
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              )}

              <button
                onClick={() => file && onAnalyze(file)}
                disabled={!file}
                className={`mt-6 w-full py-3.5 px-4 rounded-xl text-[15px] font-semibold text-white transition-all duration-300 
                  ${file ? 'glow-button hover:-translate-y-0.5 active:translate-y-0 active:scale-[0.98]' : 'bg-white/10 text-white/40 cursor-not-allowed'}`}
              >
                Analyze document
              </button>
            </>
          ) : (
            /* Loading state */
            <div className="py-8">
              <div className="flex justify-center mb-6">
                <div className="flex gap-1.5">
                  <div className="w-2.5 h-2.5 bg-primary rounded-full loading-dot" />
                  <div className="w-2.5 h-2.5 bg-primary rounded-full loading-dot" />
                  <div className="w-2.5 h-2.5 bg-primary rounded-full loading-dot" />
                </div>
              </div>
              <div className="space-y-3">
                {steps.map((step, i) => (
                  <div key={step.key} className="flex items-center gap-3">
                    <div className={`w-6 h-6 rounded-full flex items-center justify-center shrink-0 transition-all ${
                      i < currentStepIndex ? 'bg-success text-white ring-1 ring-success/30' :
                      i === currentStepIndex ? 'bg-primary text-white ring-2 ring-primary-light animate-pulse' :
                      'bg-white/10 text-white/40'
                    }`}>
                      {i < currentStepIndex ? (
                        <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                          <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                        </svg>
                      ) : (
                        <span className="text-[10px] font-bold">{i + 1}</span>
                      )}
                    </div>
                    <span className={`text-sm ${i === currentStepIndex ? 'text-text-primary font-medium' : i < currentStepIndex ? 'text-success' : 'text-text-muted'}`}>
                      {step.label}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
