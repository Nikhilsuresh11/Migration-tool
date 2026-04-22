import { getBannerStyle } from '../utils';

export default function TopBar({ filename, fileType, onReset }) {
  return (
    <div className="sticky top-0 z-30 glass-panel !border-x-0 !border-t-0 rounded-none">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg flex items-center justify-center glow-button">
            <svg className="w-4.5 h-4.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <span className="font-semibold text-[15px] tracking-wide text-white hidden sm:block">Document360 Tracker</span>
        </div>

        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 glass-panel !bg-white/5 !border-white/10 px-3 py-1.5 rounded-lg">
            <div className={`w-5 h-5 rounded text-[9px] font-bold flex items-center justify-center text-white ${fileType === 'pdf' ? 'bg-red-500/80 shadow-sm shadow-red-500/30' : 'bg-blue-500/80 shadow-sm shadow-blue-500/30'}`}>
              {fileType?.toUpperCase()}
            </div>
            <span className="text-[13px] text-white/90 font-medium max-w-[200px] truncate">{filename}</span>
          </div>
          <button
            onClick={onReset}
            className="text-sm font-semibold text-primary-light hover:text-white transition-colors flex items-center gap-1.5 px-3 py-1.5 rounded-lg hover:bg-white/10"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
            </svg>
            Analyze New
          </button>
        </div>
      </div>
    </div>
  );
}

export function MetricStrip({ metrics }) {
  const cards = [
    { label: 'Words', value: metrics.word_count?.toLocaleString() ?? '—', icon: 'M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129' },
    { label: 'Pages', value: metrics.total_pages ?? '—', icon: 'M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2' },
    { label: 'Images', value: metrics.images_count?.toLocaleString() ?? '—', icon: 'M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z' },
    { label: 'Readability', value: metrics.readability_level ?? '—', icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2' },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 -mt-3 relative z-10">
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 animate-stagger">
        {cards.map(c => (
          <div key={c.label} className="glass-panel rounded-xl p-4 transition-all hover:bg-white/5 hover:border-white/20 hover:-translate-y-1">
            <div className="flex items-center gap-2 mb-2">
              <svg className="w-4 h-4 text-primary-light" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d={c.icon} />
              </svg>
              <span className="text-[11px] font-semibold text-white/70 uppercase tracking-widest">{c.label}</span>
            </div>
            <p className="text-2xl font-bold text-white tracking-tight">{c.value}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
