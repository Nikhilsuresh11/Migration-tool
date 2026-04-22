export function formatNumber(num) {
  if (num == null) return '—';
  return num.toLocaleString();
}

export function formatFileSize(bytes) {
  if (!bytes) return '0 B';
  const units = ['B', 'KB', 'MB', 'GB'];
  let i = 0;
  let size = bytes;
  while (size >= 1024 && i < units.length - 1) {
    size /= 1024;
    i++;
  }
  return `${size.toFixed(1)} ${units[i]}`;
}

export function getGradeColor(grade) {
  switch (grade) {
    case 'A': return { bg: 'bg-success/10', text: 'text-success', border: 'border-success', solid: 'bg-success' };
    case 'B': return { bg: 'bg-warning/10', text: 'text-warning', border: 'border-warning', solid: 'bg-warning' };
    case 'C': return { bg: 'bg-warning/10', text: 'text-warning', border: 'border-warning', solid: 'bg-warning' };
    default:  return { bg: 'bg-danger/10', text: 'text-danger', border: 'border-danger', solid: 'bg-danger' };
  }
}

export function getBannerStyle(grade) {
  switch (grade) {
    case 'A': return 'from-emerald-600 to-emerald-500';
    case 'B': return 'from-amber-500 to-amber-400';
    case 'C': return 'from-amber-600 to-amber-500';
    default:  return 'from-red-600 to-red-500';
  }
}

export function getEffortColor(effort) {
  switch (effort?.toLowerCase()) {
    case 'low': return 'bg-success';
    case 'medium': return 'bg-warning';
    case 'high': return 'bg-danger';
    default: return 'bg-gray-300';
  }
}

export function getEffortWidth(effort) {
  switch (effort?.toLowerCase()) {
    case 'low': return '33%';
    case 'medium': return '66%';
    case 'high': return '100%';
    default: return '20%';
  }
}

export function copyToClipboard(text) {
  navigator.clipboard.writeText(text);
}
