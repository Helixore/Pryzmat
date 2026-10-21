const BASE_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000/api/"; // e.g. http://localhost:8000/api


let accessToken: string | null = null;

export class ApiError extends Error {
  status: number;
  details: unknown;

  constructor(status: number, details: unknown) {
    super(`Request failed: ${status}`);
    this.status = status;
    this.details = details;
  }
}

export function setAccessToken(token) {
  accessToken = token;
}

export function getAccessToken() {
  return accessToken;
}

function buildHeaders() {
  const headers = {
    "Content-Type": "application/json",
  };

  if (accessToken) {
    headers["Authorization"] = `Token ${accessToken}`;
  }

  return headers;
}

async function handleResponse<T>(response) {
  if (!response.ok) {
    let details = null;

    try {
      details = await response.json();
    } catch {
      details = null; // the error response had no JSON body
    }

    throw new ApiError(response.status, details);
  }

  // 204 No Content has no body to parse
  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export async function apiGet<T>(path) {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: buildHeaders()
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return handleResponse<T>(response);
}

export async function apiPost<T>(path, body) {
  const response = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers: buildHeaders(),
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return handleResponse<T>(response);
}