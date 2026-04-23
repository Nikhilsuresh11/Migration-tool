const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api';

/**
 * Creates a fresh FormData instance for a file.
 * Required for concurrent/sequential fetches to avoid stream issues.
 */
const createFormData = (file) => {
  const fd = new FormData();
  fd.append('file', file);
  return fd;
};

/**
 * PHASE 1: Fetch basic report summary and readiness.
 * This is the high-priority call that unlocks the Dashboard.
 * NOTE: The /api/report response already contains both `metrics` and
 *       `analysis` data from the backend, so we can use those directly
 *       instead of making separate calls.
 */
export async function fetchReportSummary(file) {
  const res = await fetch(`${API_BASE}/report`, {
    method: 'POST',
    body: createFormData(file),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    const error = new Error(err.detail || err.error || `Report phase failed (${res.status})`);
    error.status = res.status;
    throw error;
  }
  return await res.json();
}

/**
 * PHASE 2: Fetch detailed document metrics.
 * Only called when the report didn't include metrics data.
 */
export async function fetchMetrics(file) {
  const res = await fetch(`${API_BASE}/metrics`, {
    method: 'POST',
    body: createFormData(file),
  });

  if (!res.ok) {
    console.error('Metrics background fetch failed');
    return { error: 'Failed to load metrics detail' };
  }
  return await res.json();
}

/**
 * PHASE 3: Fetch deep AI analysis.
 * Only called when the report didn't include analysis data.
 */
export async function fetchAIAnalysis(file) {
  const res = await fetch(`${API_BASE}/analyze`, {
    method: 'POST',
    body: createFormData(file),
  });

  if (!res.ok) {
    console.error('AI Analysis background fetch failed');
    return { error: 'Failed to load AI analysis detail' };
  }
  return await res.json();
}

// Legacy support if needed, but we prefer unit fetchers now
export async function generateReport(file, onProgress) {
  onProgress?.('Uploading & generating summary...');
  const reportData = await fetchReportSummary(file);
  
  // We return immediately so the caller can transition UI
  // and handle metrics/analysis as side-effects.
  return { reportData, metricsData: null, analysisData: null };
}
