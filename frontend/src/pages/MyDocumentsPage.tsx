import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import Header from "../components/Header";

export default function MyDocumentsPage() {
  const [docs, setDocs] = useState<any[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    axios
      .get("http://localhost:8000/api/documents/my", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => setDocs(res.data))
      .catch(() => alert("Ошибка загрузки истории документов"));
  }, []);

  return (
    <div>
      <Header />
      <div className="p-4 max-w-4xl mx-auto">
        <h2 className="text-xl font-bold mb-4">Мои загруженные документы</h2>
        <table className="w-full border text-sm">
          <thead className="bg-gray-100">
            <tr>
              <th className="border px-2 py-1 text-left">Файл</th>
              <th className="border px-2 py-1">Дата</th>
              <th className="border px-2 py-1">Статус</th>
              <th className="border px-2 py-1">Комментарий</th>
              <th className="border px-2 py-1">Открыть</th>
            </tr>
          </thead>
          <tbody>
            {docs.map((doc) => (
              <tr key={doc.file_id}>
                <td className="border px-2 py-1">{doc.filename}</td>
                <td className="border px-2 py-1">
                  {new Date(doc.upload_time).toLocaleString()}
                </td>
                <td className="border px-2 py-1">{doc.status}</td>
                <td className="border px-2 py-1">{doc.status_comment}</td>
                <td className="border px-2 py-1 text-center">
                  <button
                    onClick={() => navigate(`/doc/${doc.file_id}`)}
                    className="text-blue-600 underline"
                  >
                    Открыть
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
