import { useState, useCallback } from 'react';
import UploadScreen from './components/UploadScreen';
import Dashboard from './components/Dashboard';
import { fetchReportSummary, fetchMetrics, fetchAIAnalysis } from './api';

export default function App() {
  const [state, setState] = useState('upload'); // upload | loading | results | error
  const [apiData, setApiData] = useState(null);
  const [loadingStep, setLoadingStep] = useState('parsing');
  const [error, setError] = useState('');

  const handleAnalyze = useCallback(async (file) => {
    setState('loading');
    setLoadingStep('parsing');
    setError('');

    try {
      // PHASE 1: The /api/report endpoint already returns metrics + analysis
      // in a single call, so we use that data directly instead of making
      // separate parallel calls that cause file-stream & rate-limit errors.
      const reportData = await fetchReportSummary(file);

      // The report response already contains `metrics` and `analysis` keys.
      // We wrap them to match the shape that MetricsTab and AiAnalysisTab expect.
      const metricsFromReport = reportData.metrics
        ? { success: true, metrics: reportData.metrics }
        : null;

      const analysisFromReport = reportData.analysis
        ? { success: true, analysis: reportData.analysis }
        : null;

      setApiData({ 
        reportData, 
        metricsData: metricsFromReport, 
        analysisData: analysisFromReport,
      });
      setState('results');

      // Only make separate calls if the report didn't include the data
      // (e.g. AI analysis timed out during the report call).
      // These are sequential to avoid file-stream corruption & rate limits.
      if (!metricsFromReport) {
        fetchMetrics(file).then(data => {
          setApiData(prev => ({ ...prev, metricsData: data }));
        });
      }

      if (!analysisFromReport) {
        // Small delay to avoid Groq rate-limiting (TPM) on back-to-back calls
        setTimeout(() => {
          fetchAIAnalysis(file).then(data => {
            setApiData(prev => ({ ...prev, analysisData: data }));
          });
        }, 2000);
      }

    } catch (err) {
      setError(err.message);
      setState('error');
    }
  }, []);

  const handleReset = useCallback(() => {
    setState('upload');
    setApiData(null);
    setError('');
    setLoadingStep('parsing');
  }, []);

  return (
    <>
      {/* Global Theme Elements */}
      <div className="space-bg"></div>
      <div className="stars"></div>

      {state === 'results' && apiData ? (
        <Dashboard data={apiData} onReset={handleReset} />
      ) : (
        <UploadScreen
          onAnalyze={handleAnalyze}
          isLoading={state === 'loading'}
          loadingStep={loadingStep}
        />
      )}

      {state === 'error' && (
        <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50 animate-fade-in">
          <div className="glass-panel rounded-xl px-5 py-3 flex items-center gap-3 max-w-md">
            <div className="w-8 h-8 bg-danger/10 rounded-lg flex items-center justify-center shrink-0">
              <svg className="w-4 h-4 text-danger" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
              </svg>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-danger">Analysis failed</p>
              <p className="text-xs text-text-muted truncate">{error}</p>
            </div>
            <button onClick={handleReset} className="text-xs text-primary font-medium hover:text-primary-dark shrink-0">
              Try again
            </button>
          </div>
        </div>
      )}
    </>
  );
}
