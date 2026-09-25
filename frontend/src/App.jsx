import { useEffect, useState } from 'react';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import ECGAnalysis from './pages/ECGAnalysis';
import ProteinAnalysis from './pages/ProteinAnalysis';
import History from './pages/History';
import Reports from './pages/Reports';
import About from './pages/About';
import { getDashboardStats, getHealth, getHistory, getReports } from './services/api';

function App() {
  const [page, setPage] = useState('Dashboard');
  const [health, setHealth] = useState('Checking backend...');
  const [stats, setStats] = useState({});
  const [history, setHistory] = useState([]);
  const [reports, setReports] = useState([]);

  useEffect(() => {
    const refreshLiveData = async () => {
      try {
        const [healthResponse, statsResponse, historyResponse, reportsResponse] = await Promise.all([
          getHealth(),
          getDashboardStats(),
          getHistory(),
          getReports(),
        ]);
        setHealth(`${healthResponse.data.service || 'API connected'} · Live`);
        setStats(statsResponse.data);
        setHistory(historyResponse.data);
        setReports(reportsResponse.data);
      } catch {
        setHealth('Backend connection unavailable');
      }
    };

    refreshLiveData();
    const refreshTimer = window.setInterval(refreshLiveData, 5000);
    return () => window.clearInterval(refreshTimer);
  }, []);

  const handleReportDeleted = (deletedId) => {
    setReports((currentReports) => currentReports.filter((report) => report.id !== deletedId));
  };

  const renderPage = () => {
    switch (page) {
      case 'ECG Analysis':
        return <ECGAnalysis />;
      case 'Protein Analysis':
        return <ProteinAnalysis />;
      case 'History':
        return <History items={history} />;
      case 'Reports':
        return <Reports items={reports} onReportDeleted={handleReportDeleted} />;
      case 'About':
        return <About />;
      case 'Dashboard':
      default:
        return <Dashboard stats={stats} history={history} onNavigate={setPage} />;
    }
  };

  return (
    <div className="app-shell">
      <Navbar currentPage={page} onNavigate={setPage} />
      <header className="topbar">
        <div>
          <h1>Cloud Science Analytics Platform</h1>
        </div>
        <span className="status-pill">{health}</span>
      </header>
      {renderPage()}
    </div>
  );
}

export default App;
