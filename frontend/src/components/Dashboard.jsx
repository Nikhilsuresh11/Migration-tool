import { useState } from 'react';
import TopBar, { MetricStrip } from './TopBar';
import OverviewTab from './OverviewTab';
import MetricsTab from './MetricsTab';
import AiAnalysisTab from './AiAnalysisTab';
import RawJsonTab from './RawJsonTab';
import D360Modal from './D360Modal';
import { copyToClipboard } from '../utils';

const TABS = [
  { key: 'overview', label: 'Overview' },
  { key: 'metrics', label: 'Metrics' },
  { key: 'analysis', label: 'AI Analysis' },
  { key: 'raw', label: 'Raw JSON' },
];

export default function Dashboard({ data, onReset }) {
  const [activeTab, setActiveTab] = useState('overview');
  const [showD360Modal, setShowD360Modal] = useState(false);

  const { reportData, metricsData, analysisData } = data;
  const { summary, metrics, analysis, filename, file_type } = reportData;

  const handleExportJson = () => {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${filename.replace(/\.[^.]+$/, '')}_bundle.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleDownloadPdf = () => {
    // Print-based PDF generation
    window.print();
  };

  return (
    <div className="min-h-screen text-white z-10 relative">
      <TopBar filename={filename} fileType={file_type} onReset={onReset} />
      <MetricStrip metrics={metrics} />

      {/* Prominent Alert Card */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 pt-8">
        <AlertCard summary={summary} />
      </div>

      {/* Tab bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 mt-8">
        <div className="border-b border-white/10 flex gap-4 overflow-x-auto">
            {TABS.map(tab => {
              const isLoading = (tab.key === 'metrics' && !metricsData) || 
                                (tab.key === 'analysis' && !analysisData);
              return (
                <button
                  key={tab.key}
                  onClick={() => setActiveTab(tab.key)}
                  className={`px-4 py-2.5 text-sm font-medium whitespace-nowrap transition-colors border-b-2 -mb-[1px] flex items-center gap-2
                    ${activeTab === tab.key
                      ? 'text-white border-primary-light shadow-[0_2px_10px_rgba(205,139,248,0.3)]'
                      : 'text-white/50 border-transparent hover:text-white/80 hover:border-white/20'}`}
                >
                  {tab.label}
                  {isLoading && (
                    <span className="flex h-2 w-2 relative">
                      <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary-light opacity-75"></span>
                      <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
                    </span>
                  )}
                </button>
              );
            })}
        </div>
      </div>

      {/* Tab content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-6">
        {activeTab === 'overview' && (
          <OverviewTab summary={summary} analysis={analysis} metrics={metrics} />
        )}
        {activeTab === 'metrics' && (
          <MetricsTab data={metricsData} />
        )}
        {activeTab === 'analysis' && (
          <AiAnalysisTab data={analysisData} />
        )}
        {activeTab === 'raw' && (
          <RawJsonTab data={data} />
        )}
      </div>

      {/* Action bar */}
      <div className="sticky bottom-0 glass-panel !border-x-0 !border-b-0 print:hidden mt-12 bg-black/40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3 flex items-center justify-end gap-3">
          <button
            onClick={handleExportJson}
            className="flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-medium bg-white/5 border border-white/10 text-white/80 hover:bg-white/10 hover:text-white transition-colors"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            Export JSON
          </button>

          <button
            onClick={handleDownloadPdf}
            className="flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-medium bg-white/5 border border-white/10 text-white/80 hover:bg-white/10 hover:text-white transition-colors"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
            </svg>
            Download PDF
          </button>

          <button
            onClick={() => setShowD360Modal(true)}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold glow-button text-white transition-all duration-200 hover:-translate-y-0.5 active:translate-y-0"
          >
            Push to Document360
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
            </svg>
          </button>
        </div>
      </div>

      <D360Modal
        isOpen={showD360Modal}
        onClose={() => setShowD360Modal(false)}
        reportData={reportData}
      />
    </div>
  );
}

function AlertCard({ summary }) {
  const { readiness_score, status_label, top_blockers, top_warnings } = summary;
  if (!status_label) return null;

  // Visual styling depending on severity
  const isDanger = readiness_score < 70;
  const isWarning = readiness_score >= 70 && readiness_score < 90;

  const bgStyle = isDanger 
    ? "bg-danger/10 border-danger/40 shadow-[0_0_15px_rgba(239,68,68,0.2)]" 
    : isWarning 
      ? "bg-warning/10 border-warning/40 shadow-[0_0_15px_rgba(249,115,22,0.2)]"
      : "bg-success/10 border-success/40 shadow-[0_0_15px_rgba(16,185,129,0.2)]";

  const iconColor = isDanger ? "text-danger" : isWarning ? "text-warning" : "text-success";

  return (
    <div className={`glass-panel border ${bgStyle} rounded-2xl p-5 sm:p-6 mb-2 animate-fade-in`}>
      <div className="flex items-start gap-4">
        <div className={`mt-1 shrink-0 ${iconColor}`}>
          {isDanger ? (
            <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          ) : isWarning ? (
            <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          ) : (
            <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          )}
        </div>
        <div className="flex-1 min-w-0">
          <h2 className="text-xl font-bold tracking-tight text-white mb-1.5">{status_label}</h2>
          {(top_blockers?.length > 0 || top_warnings?.length > 0) && (
            <p className="text-[15px] font-medium text-white/80 leading-relaxed">
              {top_blockers?.length > 0 ? top_blockers.join(' · ') : top_warnings?.join(' · ')}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
