import Cell from './Cell';
import { prettifyKey, summarizeObject } from '../utils/format';
import '../styles/nested.css';

const MAX_DEPTH = 4;

function isPlainObject(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

// Renders objects as collapsible key/value blocks and arrays as a list of
// those blocks, instead of dumping raw JSON.
export default function NestedValue({ value, depth = 0 }) {
  if (Array.isArray(value)) {
    if (value.length === 0) {
      return <span className="muted">Empty</span>;
    }

    return (
      <div className="nested-list">
        <div className="nested-count">{value.length} item(s)</div>
        {value.map((item, index) => (
          <NestedValue key={index} value={item} depth={depth + 1} />
        ))}
      </div>
    );
  }

  if (isPlainObject(value)) {
    if (depth >= MAX_DEPTH) {
      return <pre>{JSON.stringify(value, null, 2)}</pre>;
    }

    return (
      <details className="nested-object" open={depth === 0}>
        <summary>{summarizeObject(value)}</summary>
        <dl className="nested-fields">
          {Object.keys(value).map((key) => (
            <div className="nested-row" key={key}>
              <dt>{prettifyKey(key)}</dt>
              <dd>
                <NestedValue value={value[key]} depth={depth + 1} />
              </dd>
            </div>
          ))}
        </dl>
      </details>
    );
  }

  return <Cell value={value} />;
}
