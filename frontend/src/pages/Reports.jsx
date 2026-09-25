import { useState } from 'react';
import { deleteReport, downloadReport } from '../services/api';

function formatTimestamp(value) {
  if (!value) return 'Timestamp unavailable';
  return new Date(value).toLocaleString();
}

function Reports({ items = [], onReportDeleted }) {
  const [downloadError, setDownloadError] = useState('');
  const [deleteError, setDeleteError] = useState('');

  const handleDownload = async (item) => {
    try {
      setDownloadError('');
      const response = await downloadReport(item.id);
      const url = URL.createObjectURL(response.data);
      const link = document.createElement('a');
      link.href = url;
      link.download = item.file_name || `report-${item.id}.txt`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(url);
    } catch {
      setDownloadError('The report could not be downloaded.');
    }
  };

  const handleDelete = async (item) => {
    if (!window.confirm(`Delete "${item.file_name || 'this report'}"?`)) {
      return;
    }

    try {
      setDeleteError('');
      await deleteReport(item.id);
      onReportDeleted?.(item.id);
    } catch {
      setDeleteError('The report could not be deleted.');
    }
  };

  return (
    <div className="page">
      <h1>Reports</h1>
      <div className="panel">
        <h3>Generated Reports</h3>
        {downloadError && <p className="message error-message">{downloadError}</p>}
        {deleteError && <p className="message error-message">{deleteError}</p>}
        {items.length ? (
          <ul className="report-list">
            {items.map((item) => (
            <li key={item.id}>
              <span className="badge">{item.report_type || 'Report'}</span>
              <span>{item.file_name || 'Generated report'}</span>
              <time dateTime={item.created_at}>{formatTimestamp(item.created_at)}</time>
              <div className="report-actions">
                <button type="button" className="download-button" onClick={() => handleDownload(item)}>
                  Download
                </button>
                <button type="button" className="delete-button" onClick={() => handleDelete(item)}>
                  Delete
                </button>
              </div>
            </li>
            ))}
          </ul>
        ) : (
          <p className="muted">No reports generated yet.</p>
        )}
      </div>
    </div>
  );
}

export default Reports;
