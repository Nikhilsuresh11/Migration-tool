export default function MetricsTab({ data }) {
  if (!data) return <LoadingSkeleton title="Detailed Metrics" />;
  if (data.error) return <ErrorState message={data.error} />;
  const metrics = data.metrics || data;

  const basicStats = [
    { label: 'Word Count', value: metrics.word_count },
    { label: 'Paragraphs', value: metrics.paragraph_count },
    { label: 'Total Pages', value: metrics.total_pages },
    { label: 'Readability', value: metrics.readability_level },
    { label: 'Language', value: typeof metrics.language === 'object' ? (metrics.language?.primary_language || 'Unknown').toUpperCase() : (metrics.language || 'Unknown') },
  ];

  const totalLinks = (metrics.links?.internal_links || 0) + (metrics.links?.external_links || 0);

  const contentEntities = [
    { label: 'Images', value: metrics.images_count },
    { label: 'Tables', value: metrics.table_count },
    { label: 'Total Links', value: totalLinks },
    { label: 'Headings Found', value: metrics.heading_count },
  ];

  return (
    <div className="space-y-6 animate-fade-in">
      
      {/* 2-Column layout for quick stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card title="Structural Metrics">
          <div className="space-y-3">
            {basicStats.map((stat, i) => (
              <div key={i} className="flex justify-between items-center border-b border-white/5 pb-2 last:border-0 last:pb-0">
                <span className="text-sm text-white/60">{stat.label}</span>
                <span className="text-sm font-semibold text-white/90">{stat.value || 'N/A'}</span>
              </div>
            ))}
          </div>
        </Card>

        <Card title="Embedded Entities">
          <div className="space-y-3">
            {contentEntities.map((stat, i) => (
              <div key={i} className="flex justify-between items-center border-b border-white/5 pb-2 last:border-0 last:pb-0">
                <span className="text-sm text-white/60">{stat.label}</span>
                <span className="text-sm font-semibold text-white/90">{stat.value || '0'}</span>
              </div>
            ))}
          </div>
        </Card>
      </div>

      {/* Extended Table Metrics */}
      {metrics.tables && typeof metrics.tables === 'object' && metrics.table_count > 0 && (
        <Card title="Table Quality Analysis">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
             <div className="bg-white/5 border border-white/10 p-4 rounded-xl text-center">
                 <p className="text-[11px] text-white/50 uppercase tracking-widest mb-1">Total</p>
                 <p className="text-xl font-bold text-white/90">{metrics.tables.table_count || metrics.table_count}</p>
             </div>
             <div className="bg-white/5 border border-white/10 p-4 rounded-xl text-center">
                 <p className="text-[11px] text-white/50 uppercase tracking-widest mb-1">With Headers</p>
                 <p className="text-xl font-bold text-white/90">{metrics.tables.tables_with_headers || 0}</p>
             </div>
             <div className="bg-white/5 border border-white/10 p-4 rounded-xl text-center">
                 <p className="text-[11px] text-white/50 uppercase tracking-widest mb-1">Merged Cells</p>
                 <p className="text-xl font-bold text-white/90">{metrics.tables.merged_cells_detected || 0}</p>
             </div>
             <div className="bg-white/5 border border-white/10 p-4 rounded-xl text-center">
                 <p className="text-[11px] text-white/50 uppercase tracking-widest mb-1">Complex</p>
                 <p className="text-xl font-bold text-warning">{metrics.tables.complex_tables || 0}</p>
             </div>
          </div>
        </Card>
      )}

      {/* Extended Link Metrics */}
      {metrics.links && typeof metrics.links === 'object' && totalLinks > 0 && (
        <Card title="Link Quality Analysis">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
             <div className="bg-white/5 border border-white/10 p-4 rounded-xl text-center">
                 <p className="text-[11px] text-white/50 uppercase tracking-widest mb-1">Internal</p>
                 <p className="text-xl font-bold text-white/90">{metrics.links.internal_links || 0}</p>
             </div>
             <div className="bg-white/5 border border-white/10 p-4 rounded-xl text-center">
                 <p className="text-[11px] text-white/50 uppercase tracking-widest mb-1">External</p>
                 <p className="text-xl font-bold text-white/90">{metrics.links.external_links || 0}</p>
             </div>
             <div className="bg-white/5 border border-white/10 p-4 rounded-xl text-center">
                 <p className="text-[11px] text-white/50 uppercase tracking-widest mb-1">Broken</p>
                 <p className={`text-xl font-bold ${(metrics.links.broken_links || 0) > 0 ? 'text-danger' : 'text-success'}`}>{metrics.links.broken_links || 0}</p>
             </div>
             <div className="bg-white/5 border border-white/10 p-4 rounded-xl text-center">
                 <p className="text-[11px] text-white/50 uppercase tracking-widest mb-1">Cross-Refs</p>
                 <p className="text-xl font-bold text-white/90">{metrics.links.cross_document_references || 0}</p>
             </div>
          </div>
        </Card>
      )}

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

function LoadingSkeleton({ title }) {
  return (
    <div className="space-y-6 animate-pulse">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {[1, 2].map(i => (
          <div key={i} className="glass-panel rounded-xl p-6 h-48 flex flex-col gap-4">
             <div className="h-4 w-1/3 bg-white/10 rounded mb-4"></div>
             {[1, 2, 3].map(j => (
               <div key={j} className="h-3 w-full bg-white/5 rounded"></div>
             ))}
          </div>
        ))}
      </div>
      <div className="glass-panel rounded-xl p-8 h-64 flex flex-col items-center justify-center gap-4">
        <div className="w-12 h-12 rounded-full border-2 border-primary-light/20 border-t-primary-light animate-spin"></div>
        <p className="text-white/40 text-sm font-medium tracking-wide">Extracted detailed deep-metrics...</p>
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
        <p className="text-white/80 text-sm font-medium">Metrics Unavailable</p>
        <p className="text-[12px] text-white/40 mt-1">{message}</p>
      </div>
    </div>
  );
}
