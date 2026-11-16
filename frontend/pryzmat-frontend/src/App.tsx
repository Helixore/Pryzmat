import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./API/auth/authContext";
import ProtectedRoute from "./API/auth/ProtectedRoute";
import MainLayout from "./layouts/MainLayout";
import Dashboard from "./pages/Dashboard";
import Students from "./pages/Students";
import Grades from "./pages/Grades";
import LoginLayout from "./layouts/LoginLayout";

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route element={<LoginLayout />}> 
          <Route path="/login" element={<LoginLayout />}/>
        </Route>
        <Route path="/app" element={
          <ProtectedRoute>
            <MainLayout />
          </ProtectedRoute>}>
          <Route path="/app/dashboard" element={<Dashboard />} />
          <Route path="/app/students" element={<Students />} />
          <Route path="/app/grades" element={<Grades />} />
        </Route>
      </Routes>
    </AuthProvider>
  );
}