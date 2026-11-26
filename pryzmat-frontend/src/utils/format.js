// "firstName" / "first_name" -> "First name"
export function prettifyKey(key) {
  const spaced = key
    .replace(/_/g, ' ')
    .replace(/([a-z0-9])([A-Z])/g, '$1 $2')
    .toLowerCase();
  return spaced.charAt(0).toUpperCase() + spaced.slice(1);
}

const ISO_DATE = /^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}.*)?$/;

export function isIsoDate(value) {
  return typeof value === 'string' && ISO_DATE.test(value);
}

export function formatDate(value) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }

  if (value.includes('T')) {
    return date.toLocaleString('pl-PL', {
      dateStyle: 'medium',
      timeStyle: 'short',
    });
  }

  // Date-only strings are parsed as UTC, so format them as UTC too.
  return date.toLocaleDateString('pl-PL', {
    dateStyle: 'medium',
    timeZone: 'UTC',
  });
}

const LABEL_KEYS = ['name', 'title', 'label', 'theme'];
const MAX_SUMMARY_DEPTH = 2;

function isPlainObject(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

// Collects up to two short pieces describing an object: strings, numbers
// and (one level deep) summaries of nested objects.
function collectParts(value, depth) {
  const parts = [];

  for (const key of Object.keys(value)) {
    if (parts.length >= 2) {
      break;
    }
    if (key === 'id') {
      continue;
    }

    const item = value[key];

    if (typeof item === 'string' && item !== '') {
      parts.push(isIsoDate(item) ? formatDate(item) : item);
    } else if (typeof item === 'number') {
      parts.push(String(item));
    } else if (isPlainObject(item) && depth < MAX_SUMMARY_DEPTH) {
      parts.push(summarizeObject(item, depth + 1));
    }
  }

  return parts;
}

// Short label for a nested object (e.g. a teacher inside a class).
export function summarizeObject(value, depth = 0) {
  for (const key of LABEL_KEYS) {
    if (typeof value[key] === 'string' && value[key] !== '') {
      return value[key];
    }
  }

  // People: firstName + lastName
  const first = value.firstName || value.first_name || '';
  const last = value.lastName || value.last_name || '';
  const fullName = `${first} ${last}`.trim();
  if (fullName !== '') {
    return fullName;
  }

  // School class: year + symbol, e.g. "2024 A"
  if (value.year !== undefined && value.symbol !== undefined) {
    return `${value.year} ${value.symbol}`;
  }

  const parts = collectParts(value, depth);
  if (parts.length > 0) {
    return parts.join(' · ');
  }

  if (value.id !== undefined && value.id !== null) {
    return `#${value.id}`;
  }

  return 'Object';
}

// Turns any value into something safely comparable for sorting.
export function toSortable(value) {
  if (value === null || value === undefined) {
    return '';
  }
  if (Array.isArray(value)) {
    return value.length;
  }
  if (typeof value === 'object') {
    return summarizeObject(value).toLowerCase();
  }
  if (typeof value === 'string') {
    return value.toLowerCase();
  }
  return value;
}
