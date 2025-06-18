import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import UploadPage from "./pages/UploadPage";
import DocumentDetailsPage from "./pages/DocumentDetailsPage";
import MyDocumentsPage from "./pages/MyDocumentsPage";

function App() {
  const token = localStorage.getItem("token");

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to={token ? "/upload" : "/login"} />} />
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/upload"
          element={token ? <UploadPage /> : <Navigate to="/login" />}
        />
        <Route
          path="/my"
          element={token ? <MyDocumentsPage /> : <Navigate to="/login" />}
        />
        <Route
          path="/doc/:id"
          element={token ? <DocumentDetailsPage /> : <Navigate to="/login" />}
        />
        <Route path="*" element={<Navigate to="/upload" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
