import { Outlet, Link } from "react-router-dom";
import "./styles/mainLayout.css";

export default function MainLayout() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <h3>Pryzmat</h3>
        <nav>
          <ul>
            <li><Link to="/app/dashboard">Dashboard</Link></li>
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