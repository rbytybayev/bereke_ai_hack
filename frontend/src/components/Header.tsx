import { useNavigate, useLocation } from "react-router-dom";
import { jwtDecode } from "jwt-decode";

export default function Header() {
  const navigate = useNavigate();
  const location = useLocation();
  const token = localStorage.getItem("token");

  let username = "";
  try {
    if (token) {
      const decoded: any = jwtDecode(token);
      username = decoded.sub || decoded.username || "";
    }
  } catch (e) {
    username = "";
  }

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <header className="bg-gray-900 text-white px-4 py-3 flex justify-between items-center">
      <div className="text-lg font-bold">Валютный контроль</div>
      <nav className="space-x-4">
        <button onClick={() => navigate("/upload")} className="hover:underline">
          Загрузка
        </button>
        <button onClick={() => navigate("/my")} className="hover:underline">
          Мои документы
        </button>
        {username && (
          <span className="ml-4 text-sm text-gray-300">👤 {username}</span>
        )}
        {token && (
          <button onClick={handleLogout} className="ml-4 text-red-400 hover:underline">
            Выйти
          </button>
        )}
      </nav>
    </header>
  );
}
