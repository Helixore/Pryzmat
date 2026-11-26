import { useCallback, useEffect, useMemo, useState } from 'react';
import { apiFetch } from '../api/client';
import DataTable from '../components/DataTable';
import DetailModal from '../components/DetailModal';
import StateMessage from '../components/StateMessage';

const AUTO_COLUMN_LIMIT = 8;

export default function ResourceListPage({ resource }) {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [query, setQuery] = useState('');
  const [selectedRow, setSelectedRow] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const data = await apiFetch(resource.endpoint);
      // Works with and without DRF pagination.
      const list = Array.isArray(data) ? data : data.results || [];
      setRows(list);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }, [resource.endpoint]);

  useEffect(() => {
    load();
  }, [load]);

  const allKeys = useMemo(() => {
    if (rows.length === 0) {
      return [];
    }
    return Object.keys(rows[0]);
  }, [rows]);

  const columns = useMemo(() => {
    if (resource.columns) {
      return resource.columns;
    }
    return allKeys.slice(0, AUTO_COLUMN_LIMIT);
  }, [resource.columns, allKeys]);

  const filteredRows = useMemo(() => {
    const needle = query.trim().toLowerCase();
    if (needle === '') {
      return rows;
    }
    return rows.filter((row) => JSON.stringify(row).toLowerCase().includes(needle));
  }, [rows, query]);

  function renderBody() {
    if (loading) {
      return <StateMessage kind="loading" title="Loading..." />;
    }

    if (error) {
      const forbidden = error.status === 403;
      return (
        <StateMessage
          kind="error"
          title={forbidden ? 'No access' : 'Something went wrong'}
          message={
            forbidden
              ? "Your account isn't allowed to view this section."
              : error.message
          }
          onRetry={forbidden ? null : load}
        />
      );
    }

    if (rows.length === 0) {
      return (
        <StateMessage
          kind="empty"
          title="Nothing here yet"
          message={`No ${resource.label.toLowerCase()} to show.`}
        />
      );
    }

    if (filteredRows.length === 0) {
      return (
        <StateMessage
          kind="empty"
          title="No matches"
          message="Try a different search."
        />
      );
    }

    return (
      <>
        <DataTable
          rows={filteredRows}
          columns={columns}
          onRowClick={setSelectedRow}
        />
        {!resource.columns && allKeys.length > AUTO_COLUMN_LIMIT && (
          <p className="hint">
            Showing {AUTO_COLUMN_LIMIT} of {allKeys.length} fields. Click a row
            to see all of them.
          </p>
        )}
      </>
    );
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>{resource.label}</h1>
          <p className="page-subtitle">{resource.description}</p>
        </div>
        {!loading && !error && rows.length > 0 && (
          <span className="count-pill">
            {filteredRows.length === rows.length
              ? `${rows.length} total`
              : `${filteredRows.length} of ${rows.length}`}
          </span>
        )}
      </div>

      <div className="toolbar">
        <input
          className="input"
          type="search"
          placeholder={`Search ${resource.label.toLowerCase()}...`}
          value={query}
          onChange={(event) => setQuery(event.target.value)}
        />
        <button className="btn" onClick={load} disabled={loading}>
          Refresh
        </button>
      </div>

      <div className="card">{renderBody()}</div>

      {selectedRow && (
        <DetailModal
          row={selectedRow}
          title={`${resource.label} details`}
          onClose={() => setSelectedRow(null)}
        />
      )}
    </div>
  );
}
