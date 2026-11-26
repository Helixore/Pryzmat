import { useEffect, useState } from 'react';
import { ENDPOINTS } from '../api/endpoints';
import { apiFetch } from '../api/client';

// Renders any value as a short string, since the serializer shape
// (nested students / teacher) is still being worked out.
function renderCell(value) {
  if (value === null || value === undefined) {
    return '';
  }
  if (Array.isArray(value)) {
    return `${value.length} item(s)`;
  }
  if (typeof value === 'object') {
    return JSON.stringify(value);
  }
  return String(value);
}

export default function StudentClassListPage() {
  const [classes, setClasses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function load() {
      try {
        const data = await apiFetch(ENDPOINTS.studentClass);
        // Works with and without DRF pagination.
        const list = Array.isArray(data) ? data : data.results || [];
        setClasses(list);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p style={{ color: 'crimson' }}>{error}</p>;
  }

  if (classes.length === 0) {
    return <p>No classes found.</p>;
  }

  const columns = Object.keys(classes[0]);

  return (
    <div>
      <h2>Classes</h2>
      <table border="1" cellPadding="6" style={{ borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column}>{column}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {classes.map((item, index) => (
            <tr key={item.id ?? index}>
              {columns.map((column) => (
                <td key={column}>{renderCell(item[column])}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
