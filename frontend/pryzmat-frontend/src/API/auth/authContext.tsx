import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { useNavigate } from "react-router-dom";
import { apiPost, setAccessToken, setUnauthorizedHandler, setUserId, setUsername } from "./client";

interface Credentials {
  username: string;
  password: string;
}

// ADJUST: must match what your login endpoint really returns
interface LoginResponse {
  token: string;
  user_id: number;
  username: string;
  email: string;
}

interface AuthContextValue {
  isAuthenticated: boolean;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate();

  async function login(credentials: Credentials): Promise<void> {
    // ADJUST: the path to your login endpoint
    const data = await apiPost<LoginResponse>("/login", credentials);

    setAccessToken(data.token);
    setUserId(data.user_id);
    setUsername(data.username);
    setIsAuthenticated(true);
    navigate("/");
  }

  function logout(): void {
    setAccessToken(null);
    setIsAuthenticated(false);
    navigate("/login");
  }

  // If any request gets a 401, the client calls this and we log out
  useEffect(() => {
    setUnauthorizedHandler(logout);
  });

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);

  if (context === null) {
    throw new Error("useAuth must be used inside <AuthProvider>");
  }

  return context;
}