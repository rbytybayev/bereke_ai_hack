import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import Header from "../components/Header";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    setLoading(true);
    try {
      const token = localStorage.getItem("token");
      const res = await axios.post("http://localhost:8000/api/upload", formData, {
        headers: { Authorization: `Bearer ${token}` },
      });
      navigate(`/doc/${res.data.file_id}`);
    } catch (err) {
      alert("Ошибка при загрузке файла");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Header />
      <div className="flex flex-col items-center justify-center h-[calc(100vh-80px)] space-y-4">
        <h1 className="text-2xl font-bold">Загрузка валютного договора</h1>
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />
        <button
          onClick={handleUpload}
          disabled={!file || loading}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          {loading ? "Загрузка..." : "Загрузить"}
        </button>
      </div>
    </div>
  );
}
