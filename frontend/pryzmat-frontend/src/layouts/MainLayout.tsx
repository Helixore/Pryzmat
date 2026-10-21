import { Outlet, Link } from "react-router-dom";

export default function MainLayout() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <nav>
          <ul>
            <li><Link to="/app">Dashboard</Link></li>
            <li><Link to="/app/students">Uczniowie</Link></li>
            <li><Link to="/app/grades">Oceny</Link></li>
            <li><Link to="/login">Wyloguj sie</Link></li>
          </ul>
        </nav>
      </aside>

      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}