const TOKEN_KEY = 'pryzmat_token';
const USER_KEY = 'pryzmat_user';

export const UNAUTHORIZED_EVENT = 'pryzmat:unauthorized';

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function getStoredUser() {
  const raw = localStorage.getItem(USER_KEY);
  if (!raw) {
    return null;
  }
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export function saveAuth(token, user) {
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(USER_KEY, JSON.stringify(user));
}

export function clearAuth() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

export class ApiError extends Error {
  constructor(status, data) {
    super(extractMessage(data, status));
    this.status = status;
    this.data = data;
  }
}

// DRF errors come in a few shapes: {detail: "..."}, {non_field_errors: [...]},
// or {field: [...]}. This flattens them into one readable string.
function extractMessage(data, status) {
  if (!data) {
    return `Request failed (${status})`;
  }
  if (typeof data.detail === 'string') {
    return data.detail;
  }
  if (typeof data === 'object') {
    const parts = [];
    for (const key of Object.keys(data)) {
      const value = data[key];
      if (Array.isArray(value)) {
        parts.push(value.join(' '));
      } else if (typeof value === 'string') {
        parts.push(value);
      }
    }
    if (parts.length > 0) {
      return parts.join(' ');
    }
  }
  return `Request failed (${status})`;
}

export async function apiFetch(path, options = {}) {
  const token = getToken();

  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };
  if (token) {
    headers.Authorization = `Token ${token}`;
  }

  const response = await fetch(path, { ...options, headers });

  let data = null;
  if (response.status !== 204) {
    try {
      data = await response.json();
    } catch {
      data = null;
    }
  }

  if (!response.ok) {
    // A 401 on an authenticated request means the token is no longer valid.
    if (response.status === 401 && token) {
      clearAuth();
      window.dispatchEvent(new Event(UNAUTHORIZED_EVENT));
    }
    throw new ApiError(response.status, data);
  }

  return data;
}
