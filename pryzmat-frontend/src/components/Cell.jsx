import { formatDate, isIsoDate, summarizeObject } from '../utils/format';

export default function Cell({ value }) {
  if (value === null || value === undefined || value === '') {
    return <span className="muted">—</span>;
  }

  if (typeof value === 'boolean') {
    return (
      <span className={value ? 'badge badge-green' : 'badge badge-gray'}>
        {value ? 'Yes' : 'No'}
      </span>
    );
  }

  if (Array.isArray(value)) {
    return <span className="badge badge-blue">{value.length} item(s)</span>;
  }

  if (typeof value === 'object') {
    return <span className="badge badge-blue">{summarizeObject(value)}</span>;
  }

  if (isIsoDate(value)) {
    return <span>{formatDate(value)}</span>;
  }

  return <span className="cell-text">{String(value)}</span>;
}
