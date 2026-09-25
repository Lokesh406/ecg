function History({ items }) {
  return (
    <div className="page">
      <h1>History</h1>
      <div className="panel">
        <table className="history-table">
          <thead>
            <tr>
              <th>Type</th>
              <th>Name</th>
              <th>Date</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {(items || []).map((item, index) => (
              <tr key={`${item.type}-${item.name}-${index}`}>
                <td>{item.type}</td>
                <td>{item.name}</td>
                <td>{item.date || '23/09/26'}</td>
                <td>{item.status || 'Completed'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default History;
