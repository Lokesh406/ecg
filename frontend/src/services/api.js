import api from '../api/client';

export const getHealth = () => api.get('/api/health');

export const getDashboardStats = () => api.get('/api/dashboard/stats');
export const getHistory = () => api.get('/api/history');
export const getReports = () => api.get('/api/reports');
export const deleteReport = (reportId) => api.delete(`/api/reports/${reportId}`);
export const downloadReport = (reportId) => api.get(`/api/reports/${reportId}/download`, {
  responseType: 'blob',
});

export const uploadECG = (file) => {
  const form = new FormData();
  form.append('file', file);
  return api.post('/api/ecg/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const analyzeECG = () => api.post('/api/ecg/analyze');

export const uploadProtein = (file) => {
  const form = new FormData();
  form.append('file', file);
  return api.post('/api/protein/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const analyzeProtein = () => api.post('/api/protein/analyze');
