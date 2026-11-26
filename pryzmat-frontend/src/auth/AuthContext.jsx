import { createContext, useContext, useEffect, useState } from 'react';
import { ENDPOINTS } from '../api/endpoints';
import {
  apiFetch,
  clearAuth,
  getStoredUser,
  saveAuth,
  UNAUTHORIZED_EVENT,
} from '../api/client';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(getStoredUser());

  useEffect(() => {
    function handleUnauthorized() {
      setUser(null);
    }
    window.addEventListener(UNAUTHORIZED_EVENT, handleUnauthorized);
    return () => {
      window.removeEventListener(UNAUTHORIZED_EVENT, handleUnauthorized);
    };
  }, []);

  async function login(username, password) {
    const data = await apiFetch(ENDPOINTS.login, {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });

    const loggedInUser = {
      id: data.user_id,
      username: data.username,
      email: data.email,
      role: data.role,
    };

    saveAuth(data.token, loggedInUser);
    setUser(loggedInUser);
  }

  function logout() {
    clearAuth();
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used inside AuthProvider');
  }
  return context;
}
