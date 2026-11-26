import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './auth/AuthContext';
import ProtectedRoute from './auth/ProtectedRoute';
import { RESOURCES } from './api/resources';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import ResourceListPage from './pages/ResourceListPage';

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />

          <Route
            element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }
          >
            <Route path="/" element={<HomePage />} />

            {RESOURCES.map((resource) => (
              <Route
                key={resource.key}
                path={`/${resource.path}`}
                element={
                  <ProtectedRoute allowedRoles={resource.roles}>
                    {/* key forces a fresh page (search, sort) per resource */}
                    <ResourceListPage key={resource.key} resource={resource} />
                  </ProtectedRoute>
                }
              />
            ))}
          </Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
