import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import Header from "../components/Header";

export default function DocumentDetailsPage() {
  const { id } = useParams();
  const [data, setData] = useState<any>(null);
  const [status, setStatus] = useState("");
  const [comment, setComment] = useState("");

  const token = localStorage.getItem("token");

  useEffect(() => {
    axios
      .get(`/api/documents/${id}`, { headers: { Authorization: `Bearer ${token}` } })
      .then((res) => setData(res.data))
      .catch(() => alert("Ошибка при получении данных документа"));
  }, [id]);

  const handleStatusUpdate = async () => {
    try {
      await axios.post(
        "/api/update_status",
        {
          file_id: id,
          new_status: status,
          comment: comment,
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert("Статус обновлён");
    } catch (e) {
      alert("Ошибка при обновлении статуса");
    }
  };

  if (!data) return <div className="p-4">Загрузка...</div>;

  return (
    <div>
      <Header />
      <div className="p-4 max-w-4xl mx-auto space-y-4">
        <h2 className="text-xl font-bold">Информация по документу</h2>
        <p><b>Имя файла:</b> {data.filename}</p>
        <p><b>Язык:</b> {data.language}</p>
        <p><b>Подпись:</b> {data.has_signature ? "Есть" : "Нет"}</p>

        <h3 className="text-lg font-semibold mt-4">Параметры договора:</h3>
        <pre className="bg-gray-100 p-2 rounded text-sm whitespace-pre-wrap">
          {JSON.stringify(data.contract_data, null, 2)}
        </pre>

        <h3 className="text-lg font-semibold">Результаты проверок:</h3>
        <ul className="list-disc pl-6">
          {data.checks.map((c: any, idx: number) => (
            <li key={idx} className={c.status === "fail" ? "text-red-600" : "text-green-600"}>
              {c.name}: {c.status} {c.reason ? `– ${c.reason}` : ""}
            </li>
          ))}
        </ul>

        <h3 className="text-lg font-semibold">Вердикт:</h3>
        <p className="border-l-4 border-blue-500 bg-blue-50 p-3 rounded">
          {data.verdict.summary}
        </p>
        <p className="font-bold">Итог: {data.verdict.decision}</p>

        <div className="mt-6 border-t pt-4">
          <h4 className="font-semibold mb-2">Изменить статус вручную:</h4>
          <select value={status} onChange={(e) => setStatus(e.target.value)} className="border p-2 rounded">
            <option value="">Выберите статус</option>
            <option value="Принят">Принят</option>
            <option value="Отказано">Отказано</option>
          </select>
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="Комментарий"
            className="border p-2 rounded w-full mt-2"
          />
          <button onClick={handleStatusUpdate} className="bg-blue-600 text-white px-4 py-2 mt-2 rounded">
            Сохранить
          </button>
        </div>
      </div>
    </div>
  );
}
