import { NavLink, Outlet } from 'react-router-dom';
import { useAuth } from '../auth/AuthContext';
import { GROUPS, resourcesForRole } from '../api/resources';

export default function Layout() {
  const { user, logout } = useAuth();

  const available = resourcesForRole(user.role);

  const navGroups = GROUPS.map((groupName) => ({
    name: groupName,
    items: available.filter((resource) => resource.group === groupName),
  })).filter((group) => group.items.length > 0);

  const initial = user.username.charAt(0).toUpperCase();

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-logo">P</div>
          <span className="brand-name">Pryzmat</span>
        </div>

        <nav className="nav">
          <NavLink to="/" end className="nav-link">
            Home
          </NavLink>

          {navGroups.map((group) => (
            <div key={group.name} className="nav-group">
              <div className="nav-group-label">{group.name}</div>
              {group.items.map((resource) => (
                <NavLink
                  key={resource.key}
                  to={`/${resource.path}`}
                  className="nav-link"
                >
                  {resource.label}
                </NavLink>
              ))}
            </div>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="avatar">{initial}</div>
          <div className="user-info">
            <div className="user-name">{user.username}</div>
            <div className="user-role">{user.role || 'no role'}</div>
          </div>
          <button className="btn btn-ghost" onClick={logout}>
            Log out
          </button>
        </div>
      </aside>

      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}
