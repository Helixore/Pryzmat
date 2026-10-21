import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainLayout from "./layouts/MainLayout";
import Dashboard from "./pages/Dashboard";
import Students from "./pages/Students";
import Grades from "./pages/Grades";
import LoginLayout from "./layouts/LoginLayout";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<LoginLayout />}> 
          <Route path="/login" element={<LoginLayout />}/>
        </Route>
        <Route element={<MainLayout />}>
          <Route path="/app" element={<Dashboard />} />
          <Route path="/app/students" element={<Students />} />
          <Route path="/app/grades" element={<Grades />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}