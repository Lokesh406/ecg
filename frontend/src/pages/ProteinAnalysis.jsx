import { useState } from 'react';
import { Bar, BarChart, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { uploadProtein, analyzeProtein } from '../services/api';

function ProteinAnalysis() {
  const [file, setFile] = useState(null);
  const [sequence, setSequence] = useState('MKTIIALSYIFCLVFADYKDDDDK');
  const [result, setResult] = useState(null);
  const [message, setMessage] = useState('');

  const structureData = result?.secondary_structure
    ? [...result.secondary_structure].map((type, index) => ({
      position: index + 1,
      type,
      value: type === 'H' ? 3 : type === 'E' ? 2 : 1,
    }))
    : [];

  const hydrophobicityData = result
    ? [{ name: 'Hydrophobicity', value: Number(result.hydrophobicity) || 0 }]
    : [];

  const handleUpload = async () => {
    if (!file) {
      setMessage('Please select a FASTA or text file first.');
      return;
    }

    try {
      const response = await uploadProtein(file);
      setMessage(`Upload successful: ${response.data.protein_name}`);
      const analysis = await analyzeProtein();
      setResult(analysis.data);
    } catch (error) {
      setMessage(error.response?.data?.detail || 'Protein upload failed.');
    }
  };

  return (
    <div className="page">
      <h1>Protein Analysis</h1>
      <div className="panel">
        <h3>Enter Protein Sequence</h3>
        <textarea
          rows="5"
          value={sequence}
          onChange={(e) => setSequence(e.target.value)}
          placeholder="MKTIIALSYIFCLVFADYKDDDDK"
        />
        <input type="file" accept=".fasta,.fa,.txt" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={handleUpload}>Analyze Protein</button>
        {message && <p className="message">{message}</p>}
      </div>

      {result && (
        <>
          <div className="panel chart-panel">
            <div className="panel-heading">
              <div>
                <span className="eyebrow">Sequence map</span>
                <h3>Secondary structure profile</h3>
              </div>
              <span className="chart-meta">H helix · E sheet · C coil</span>
            </div>
            <div className="chart-frame structure-chart">
              <ResponsiveContainer width="100%" height={180}>
                <BarChart data={structureData} barCategoryGap={1}>
                  <XAxis dataKey="position" tickLine={false} axisLine={false} />
                  <YAxis hide domain={[0, 3]} />
                  <Tooltip formatter={(value, name, item) => [item.payload.type, 'Structure']} />
                  <Bar dataKey="value" radius={[3, 3, 0, 0]}>
                    {structureData.map((item) => (
                      <Cell key={item.position} fill={item.type === 'H' ? '#38bdf8' : item.type === 'E' ? '#fbbf24' : '#a78bfa'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div className="hydrophobicity-row">
              <span>Hydrophobicity</span>
              <div className="hydrophobicity-chart">
                <ResponsiveContainer width="100%" height={44}>
                  <BarChart data={hydrophobicityData} layout="vertical" margin={{ left: 0, right: 8 }}>
                    <XAxis type="number" hide domain={[0, 'dataMax']} />
                    <YAxis type="category" dataKey="name" hide />
                    <Bar dataKey="value" fill="#34d399" radius={[0, 6, 6, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
              <strong>{Number(result.hydrophobicity).toFixed(3)}</strong>
            </div>
          </div>

          <div className="panel result-panel">
            <h3>Analysis Result</h3>
          <p><strong>Protein:</strong> {result.protein_name}</p>
          <p><strong>Sequence Length:</strong> {result.sequence_length}</p>
          <p><strong>Molecular Weight:</strong> {result.molecular_weight}</p>
          <p><strong>Hydrophobicity:</strong> {result.hydrophobicity}</p>
          <p><strong>Secondary Structure:</strong> {result.secondary_structure}</p>
          <p className="disclaimer">{result.disclaimer}</p>
          </div>
        </>
      )}
    </div>
  );
}

export default ProteinAnalysis;
