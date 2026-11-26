import { Link } from 'react-router-dom';
import { useAuth } from '../auth/AuthContext';
import { resourcesForRole } from '../api/resources';

export default function HomePage() {
  const { user } = useAuth();

  if (!user.role) {
    return (
      <div className="card card-padded">
        <h2>No role assigned</h2>
        <p className="muted">
          This account isn't linked to a teacher, parent, student, principal or
          worker profile yet.
        </p>
      </div>
    );
  }

  const available = resourcesForRole(user.role);

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Welcome back, {user.username}</h1>
          <p className="page-subtitle">
            Signed in as <span className="badge badge-blue">{user.role}</span>
          </p>
        </div>
      </div>

      <div className="tile-grid">
        {available.map((resource) => (
          <Link key={resource.key} to={`/${resource.path}`} className="tile">
            <div className="tile-group">{resource.group}</div>
            <div className="tile-title">{resource.label}</div>
            <div className="tile-description">{resource.description}</div>
          </Link>
        ))}
      </div>
    </div>
  );
}
