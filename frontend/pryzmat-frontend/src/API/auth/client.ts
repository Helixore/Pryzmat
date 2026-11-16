const BASE_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000/api/"; // e.g. http://localhost:8000/api


let accessToken: string | null = null;
let userId: number | null = null;
let username: string | null = null;

let onUnauthorized: (() => void) | null = null;

export class ApiError extends Error {
  status: number;
  details: unknown;

  constructor(status: number, details: unknown) {
    super(`Request failed: ${status}`);
    this.status = status;
    this.details = details;
  }
}

export function setAccessToken(token: string | null) {
  accessToken = token;
}
export function setUserId(id: number | null){
  userId = id;
}
export function setUsername(uname: string | null){
  username = uname;
}

export function getAccessToken() {
  return accessToken;
}
export function getUserId() {
  return userId;
}

export function getUsername() {
  return username;
}


export function setUnauthorizedHandler(handler: (() => void) | null): void {
  onUnauthorized = handler;
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  if (accessToken) {
    headers["Authorization"] = `Token ${accessToken}`;
  }

  const response = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: headers,
  });

  if (!response.ok) {
    // Expired or invalid token while logged in -> force logout.
    // A wrong password on the login form has no token yet, so it skips this.
    if (response.status === 401 && accessToken && onUnauthorized) {
      onUnauthorized();
    }

    let details: unknown = null;
    try {
      details = await response.json();
    } catch {
      details = null;
    }

    throw new ApiError(response.status, details);
  }

  // 204 No Content has no body to parse
  if (response.status === 204) {
    return null as T;
  }

  return response.json() as Promise<T>;
}

export function apiGet<T>(path: string): Promise<T> {
  return request<T>(path);
}

export function apiPost<T>(path: string, body: unknown): Promise<T> {
  return request<T>(path, {
    method: "POST",
    body: JSON.stringify(body),
  });
}