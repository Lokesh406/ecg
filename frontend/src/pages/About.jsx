function About() {
  return (
    <div className="page">
      <h1>About</h1>
      <div className="panel">
        <h3>What is cloud computing?</h3>
        <p>Cloud computing provides on-demand access to remote computing, storage, and analytics services over the internet.</p>

        <h3>Why is it useful for scientific applications?</h3>
        <p>It allows researchers and students to process large datasets, store results in remote storage, and deploy scientific applications without owning expensive physical infrastructure.</p>

        <h3>How ECG analysis uses cloud computing</h3>
        <p>ECG data is uploaded to a cloud platform, processed remotely using signal-analysis algorithms, and results are stored centrally for reporting and comparison.</p>

        <h3>How protein analysis uses cloud computing</h3>
        <p>Protein sequences can be processed in the cloud for composition, hydrophobicity, and secondary-structure analysis without requiring local high-performance resources.</p>

        <h3>AWS S3 and EC2 roles</h3>
        <p>S3 stores uploaded data and reports, while EC2 hosts the backend and frontend application. IAM controls access securely without embedding credentials in code.</p>
      </div>
    </div>
  );
}

export default About;
