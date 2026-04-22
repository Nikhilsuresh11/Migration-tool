export default function OverviewTab({ summary, analysis, metrics }) {
  return (
    <div className="space-y-6 animate-fade-in">
      {/* Row 1: Score ring */}
      <div>
        <ScoreRing score={summary.readiness_score} />
      </div>

      {/* Row 2: Visual stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <VisualStats analysis={analysis} metrics={metrics} />
      </div>

    </div>
  );
}

function ScoreRing({ score }) {
  const getColorText = (s) => {
    if (s >= 90) return 'text-success';
    if (s >= 75) return 'text-primary';
    if (s >= 60) return 'text-warning';
    return 'text-danger';
  };
  const strokeClass = getColorText(score).replace('text-', 'stroke-');
  const circumference = 283;
  const offset = circumference - (circumference * score) / 100;

  return (
    <Card title="Readiness Score">
      <div className="flex items-center justify-center py-4">
        <div className="relative w-36 h-36">
          <svg className="w-full h-full -rotate-90" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="45" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="8" />
            <circle
              cx="50" cy="50" r="45" fill="none"
              strokeWidth="8" strokeLinecap="round"
              className={`${strokeClass}`}
              strokeDasharray={circumference}
              strokeDashoffset={offset}
              style={{ animation: 'score-fill 1.2s ease-out forwards', strokeDashoffset: offset }}
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="text-4xl font-bold text-white">{score}</span>
            <span className="text-xs text-white/60">of 100</span>
          </div>
        </div>
      </div>
    </Card>
  );
}





function VisualStats({ analysis, metrics }) {
  const visual = analysis?.visual_content_analysis || {};
  const pairs = [
    { label: 'Image-to-text ratio', value: visual.image_to_text_ratio },
    { label: 'Decorative images', value: visual.images_likely_decorative },
    { label: 'Informational images', value: visual.images_likely_informational },
    { label: 'Accessibility risk', value: visual.accessibility_risk },
    { label: 'Tables', value: metrics.table_count },
    { label: 'Images with alt text', value: visual.images_with_alt_text },
  ];

  return (
    <Card title="Visual Content">
      <div className="space-y-2.5">
        {pairs.map(p => (
          <div key={p.label} className="flex justify-between gap-2 border-b border-white/5 pb-2 last:border-0 last:pb-0">
            <span className="text-xs font-medium text-white/60">{p.label}</span>
            <span className="text-xs text-white/90 font-medium text-right">{p.value ?? '—'}</span>
          </div>
        ))}
      </div>
      {visual.migration_recommendation && (
        <p className="mt-3 text-[11px] text-primary-light bg-primary/20 border border-primary/30 px-3 py-2 rounded-lg">
          💡 {visual.migration_recommendation}
        </p>
      )}
    </Card>
  );
}

/* Shared card wrapper */
function Card({ title, badge, children }) {
  return (
    <div className="glass-panel rounded-xl p-5 transition-colors hover:bg-white/5">
      <div className="flex items-center justify-between mb-4 border-b border-white/10 pb-3">
        <h3 className="text-[15px] font-semibold text-white tracking-wide">{title}</h3>
        {badge && <span className="text-[11px] font-medium text-primary-light bg-primary/20 border border-primary/30 px-2 py-0.5 rounded">{badge}</span>}
      </div>
      {children}
    </div>
  );
}

function EmptyCard({ title, message }) {
  return (
    <Card title={title}>
      <div className="text-sm text-white/50 py-4 text-center">{message}</div>
    </Card>
  );
}
