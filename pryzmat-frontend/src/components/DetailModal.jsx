import { useEffect } from 'react';
import NestedValue from './NestedValue';
import { prettifyKey } from '../utils/format';

export default function DetailModal({ row, title, onClose }) {
  useEffect(() => {
    function handleKeyDown(event) {
      if (event.key === 'Escape') {
        onClose();
      }
    }
    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [onClose]);

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        className="modal"
        onClick={(event) => event.stopPropagation()}
        role="dialog"
        aria-modal="true"
      >
        <div className="modal-header">
          <h3>{title}</h3>
          <button className="btn btn-ghost" onClick={onClose}>
            Close
          </button>
        </div>

        <dl className="detail-list">
          {Object.keys(row).map((key) => (
            <div className="detail-row" key={key}>
              <dt>{prettifyKey(key)}</dt>
              <dd>
                <NestedValue value={row[key]} />
              </dd>
            </div>
          ))}
        </dl>
      </div>
    </div>
  );
}
