import { useState } from 'react';
import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { uploadECG, analyzeECG } from '../services/api';

function ECGAnalysis() {
  const [file, setFile] = useState(null);
  const [waveform, setWaveform] = useState([]);
  const [result, setResult] = useState(null);
  const [message, setMessage] = useState('');

  const handleFileChange = async (event) => {
    const selectedFile = event.target.files[0];
    setFile(selectedFile || null);
    setResult(null);
    if (!selectedFile) {
      setWaveform([]);
      return;
    }

    const content = await selectedFile.text();
    const values = content
      .split(/\r?\n/)
      .slice(1)
      .map((value) => Number(value.trim()))
      .filter((value) => Number.isFinite(value));
    setWaveform(values.map((value, index) => ({ sample: index + 1, value })));
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage('Please select a CSV ECG file first.');
      return;
    }

    try {
      const response = await uploadECG(file);
      setMessage(`Upload successful: ${response.data.file_name}`);
      const analysis = await analyzeECG();
      setResult(analysis.data);
    } catch (error) {
      setMessage(error.response?.data?.detail || 'ECG upload failed.');
    }
  };

  return (
    <div className="page">
      <h1>ECG Analysis</h1>
      <div className="panel">
        <h3>Upload ECG CSV</h3>
        <input type="file" accept=".csv" onChange={handleFileChange} />
        <button onClick={handleUpload}>Upload and Analyze</button>
        {message && <p className="message">{message}</p>}
      </div>

      {waveform.length > 0 && result && (
        <div className="panel chart-panel">
          <div className="panel-heading">
            <div>
              <span className="eyebrow">Live analysis output</span>
              <h3>Analyzed ECG waveform</h3>
            </div>
            <span className="chart-meta">
              {waveform.length} samples · {result.peak_count} detected peaks
            </span>
          </div>
          <div className="chart-frame">
            <ResponsiveContainer width="100%" height={280}>
              <LineChart data={waveform} margin={{ top: 12, right: 18, left: 0, bottom: 8 }}>
                <XAxis dataKey="sample" tickLine={false} axisLine={false} />
                <YAxis tickLine={false} axisLine={false} width={42} />
                <Tooltip contentStyle={{ background: '#111827', border: '1px solid #334155' }} />
                <Line type="monotone" dataKey="value" stroke="#38bdf8" strokeWidth={2.5} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {result && (
        <div className="panel result-panel">
          <h3>Analysis Result</h3>
          <p><strong>File:</strong> {result.file_name}</p>
          <p><strong>Heart Rate:</strong> {result.heart_rate}</p>
          <p><strong>Peak Count:</strong> {result.peak_count}</p>
          <p><strong>Classification:</strong> {result.classification}</p>
          <p className="disclaimer">{result.disclaimer}</p>
        </div>
      )}
    </div>
  );
}

export default ECGAnalysis;
