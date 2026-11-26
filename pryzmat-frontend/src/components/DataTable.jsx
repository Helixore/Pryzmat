import { useMemo, useState } from 'react';
import Cell from './Cell';
import { prettifyKey, toSortable } from '../utils/format';

export default function DataTable({ rows, columns, onRowClick }) {
  const [sortKey, setSortKey] = useState(null);
  const [sortDirection, setSortDirection] = useState('asc');

  const sortedRows = useMemo(() => {
    if (!sortKey) {
      return rows;
    }

    const copy = [...rows];
    copy.sort((a, b) => {
      const left = toSortable(a[sortKey]);
      const right = toSortable(b[sortKey]);

      if (left < right) {
        return sortDirection === 'asc' ? -1 : 1;
      }
      if (left > right) {
        return sortDirection === 'asc' ? 1 : -1;
      }
      return 0;
    });
    return copy;
  }, [rows, sortKey, sortDirection]);

  function handleSort(key) {
    if (sortKey === key) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortKey(key);
      setSortDirection('asc');
    }
  }

  function sortIndicator(key) {
    if (sortKey !== key) {
      return '';
    }
    return sortDirection === 'asc' ? ' ▲' : ' ▼';
  }

  return (
    <div className="table-wrap">
      <table className="table">
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column} onClick={() => handleSort(column)}>
                {prettifyKey(column)}
                {sortIndicator(column)}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sortedRows.map((row, index) => (
            <tr key={row.id ?? index} onClick={() => onRowClick(row)}>
              {columns.map((column) => (
                <td key={column}>
                  <Cell value={row[column]} />
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
