export default function AiAnalysisTab({ data }) {
  if (!data) return <LoadingSkeleton />;
  if (data.error) return <ErrorState message={data.error} />;
  const analysis = data.analysis || data;

  const debt = analysis.content_debt || {};
  const tone = analysis.tone_analysis || {};
  const docClass = analysis.content_classification || {};

  return (
    <div className="space-y-6 animate-fade-in">
      
      {/* Classification Card */}
      <Card title="Document Classification">
        <div className="flex flex-col md:flex-row gap-6 items-start md:items-center">
            <div className="flex-1">
                <span className="text-xs font-semibold text-primary-light bg-primary/10 border border-primary/20 px-2 py-1 rounded">
                    {docClass.document_type || 'Unknown Type'}
                </span>
                <h4 className="text-lg font-medium text-white mt-3 mb-1">
                    {docClass.domain || 'Unknown Domain'}
                </h4>
                <p className="text-sm text-white/60">
                    {docClass.audience_type || 'General Audience'}
                </p>
            </div>
            {analysis.readability_level && (
              <div className="bg-white/5 border border-white/10 px-4 py-3 rounded-xl shrink-0 text-center">
                  <div className="text-[11px] text-white/60 uppercase tracking-widest font-semibold mb-1">Readability</div>
                  <div className="text-lg font-bold text-white tracking-tight">{analysis.readability_level}</div>
              </div>
            )}
        </div>
      </Card>

      {/* Tone and Debt */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card title="Tone Analysis">
            <div className="space-y-4">
               <div>
                 <div className="flex justify-between items-center mb-1">
                    <span className="text-sm text-white/70">Passive Voice Usage</span>
                    <span className="text-sm font-semibold text-white/90">{tone.passive_voice_ratio_percent ?? 0}%</span>
                 </div>
                 <div className="h-1.5 bg-white/10 rounded-full overflow-hidden">
                    <div 
                        className={`h-full rounded-full transition-all duration-700 ${tone.passive_voice_ratio_percent > 40 ? 'bg-warning/80' : 'bg-success/80'}`}
                        style={{ width: `${Math.min(tone.passive_voice_ratio_percent || 0, 100)}%` }}
                    />
                 </div>
               </div>
               {tone.tone_tags && tone.tone_tags.length > 0 && (
                   <div>
                       <span className="text-xs text-white/50 block mb-2">Detected Tones</span>
                       <div className="flex flex-wrap gap-2">
                           {tone.tone_tags.map((t, i) => (
                               <span key={i} className="text-[11px] bg-white/5 border border-white/10 text-white/80 px-2 py-1 rounded-md">
                                   {t}
                               </span>
                           ))}
                       </div>
                   </div>
               )}
            </div>
        </Card>

        <Card title="Content Debt Index" badge={`Score: ${debt.content_debt_score || 0}/10`}>
             <div className="space-y-3">
                <DebtRow label="Undefined Abbreviations" val={debt.abbreviations_without_definition?.length} />
                <DebtRow label="Outdated References" val={debt.outdated_references_detected?.length} />
                <DebtRow label="Unresolved Placeholders" val={debt.unresolved_placeholders?.length} />
                <DebtRow label="Broken Cross-References" val={debt.broken_concept_references} />
             </div>
        </Card>
      </div>

    </div>
  );
}

function DebtRow({ label, val }) {
    const num = typeof val === 'number' ? val : (val?.length || 0);
    return (
        <div className="flex justify-between items-center border-b border-white/5 pb-2 last:border-0 last:pb-0">
            <span className="text-sm text-white/60">{label}</span>
            <span className={`text-sm font-semibold ${num > 0 ? 'text-warning' : 'text-success'}`}>{num}</span>
        </div>
    );
}

function Card({ title, badge, children }) {
  return (
    <div className="glass-panel rounded-xl p-5 transition-colors hover:bg-white/5 h-full">
      <div className="flex items-center justify-between mb-4 border-b border-white/10 pb-3">
        <h3 className="text-[15px] font-semibold text-white tracking-wide">{title}</h3>
        {badge && <span className="text-[11px] font-medium text-primary-light bg-primary/20 border border-primary/30 px-2 py-0.5 rounded">{badge}</span>}
      </div>
      {children}
    </div>
  );
}

function LoadingSkeleton() {
  return (
    <div className="space-y-6 animate-pulse">
      <div className="glass-panel rounded-xl p-6 h-32 flex items-center gap-6">
         <div className="w-16 h-16 rounded-lg bg-white/10"></div>
         <div className="flex-1 space-y-3">
             <div className="h-4 w-1/4 bg-white/10 rounded"></div>
             <div className="h-3 w-1/2 bg-white/5 rounded"></div>
         </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {[1, 2].map(i => (
          <div key={i} className="glass-panel rounded-xl p-6 h-48 flex flex-col gap-4">
             <div className="h-4 w-1/3 bg-white/10 rounded mb-2"></div>
             <div className="h-2 w-full bg-white/5 rounded"></div>
             <div className="h-2 w-2/3 bg-white/5 rounded"></div>
             <div className="h-2 w-full bg-white/5 rounded"></div>
          </div>
        ))}
      </div>

      <div className="glass-panel rounded-xl p-8 h-48 flex flex-col items-center justify-center gap-4 border border-primary/20 bg-primary/5">
        <div className="relative">
            <div className="w-10 h-10 rounded-full border-2 border-primary-light/10 border-t-primary-light animate-spin"></div>
            <div className="absolute inset-0 flex items-center justify-center">
                <div className="w-1 h-1 bg-primary-light rounded-full animate-ping"></div>
            </div>
        </div>
        <div className="text-center">
            <p className="text-white/60 text-sm font-medium tracking-wide">AI is thinking...</p>
            <p className="text-[10px] text-white/30 uppercase mt-1 tracking-widest">Applying Document360 heuristics</p>
        </div>
      </div>
    </div>
  );
}

function ErrorState({ message }) {
  return (
    <div className="glass-panel rounded-xl p-8 flex flex-col items-center justify-center gap-4 border border-danger/20 bg-danger/5">
      <svg className="w-10 h-10 text-danger/60" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
      </svg>
      <div className="text-center">
        <p className="text-white/80 text-sm font-medium">AI Analysis Unavailable</p>
        <p className="text-[12px] text-white/40 mt-1">{message}</p>
      </div>
    </div>
  );
}
