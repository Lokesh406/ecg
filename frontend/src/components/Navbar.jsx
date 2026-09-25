function Navbar({ currentPage, onNavigate }) {
  const items = [
    'Dashboard',
    'ECG Analysis',
    'Protein Analysis',
    'History',
    'Reports',
    'About',
  ];

  return (
    <nav className="navbar">
      <div className="brand">Cloud Science Analytics Platform</div>
      <div className="nav-items">
        {items.map((item) => (
          <button
            key={item}
            className={currentPage === item ? 'nav-button active' : 'nav-button'}
            onClick={() => onNavigate(item)}
          >
            {item}
          </button>
        ))}
      </div>
    </nav>
  );
}

export default Navbar;
