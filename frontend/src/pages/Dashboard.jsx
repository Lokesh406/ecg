function Dashboard({ stats, history, onNavigate }) {
  return (
    <div className="page">
      <h1>Dashboard</h1>
      <div className="stats-grid">
        <div className="stat-box accent-blue">
          <span>Total ECG Analyses</span>
          <strong>{stats?.ecg_analyses ?? 0}</strong>
        </div>
        <div className="stat-box accent-green">
          <span>Total Protein Analyses</span>
          <strong>{stats?.protein_analyses ?? 0}</strong>
        </div>
        <div className="stat-box accent-purple">
          <span>Files Stored</span>
          <strong>{stats?.files_stored ?? 0}</strong>
        </div>
        <div className="stat-box accent-gold">
          <span>Reports Generated</span>
          <strong>{stats?.reports_generated ?? 0}</strong>
        </div>
      </div>

      <div className="module-grid">
        <div className="module-card large ecg">
          <h2>🫀 ECG Analysis</h2>
          <p>Upload ECG files, detect peaks, calculate heart rate, and review waveform metrics.</p>
          <button onClick={() => onNavigate && onNavigate('ECG Analysis')}>Open ECG Analysis</button>
        </div>

        <div className="module-card large protein">
          <h2>🧬 Protein Analysis</h2>
          <p>Analyze sequence composition, molecular weight, hydrophobicity, and secondary structure.</p>
          <button onClick={() => onNavigate && onNavigate('Protein Analysis')}>Open Protein Analysis</button>
        </div>
      </div>

      <div className="panel">
        <h3>Recent Activity</h3>
        <ul className="activity-list">
          {(history || []).slice(0, 6).map((item, index) => (
            <li key={`${item.type}-${item.name}-${index}`}>
              <span className="badge">{item.type}</span>
              <span>{item.name}</span>
              <span className="muted">{item.date || 'Completed'}</span>
              <span className="status">{item.status || 'Completed'}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default Dashboard;
