import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isRegister, setIsRegister] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const url = isRegister ? "/api/auth/register" : "/api/auth/token";
    try {
      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("password", password);
      const res = await axios.post(url, formData);
      if (!isRegister) {
        localStorage.setItem("token", res.data.access_token);
        navigate("/upload");
      } else {
        alert("Регистрация успешна, войдите.");
        setIsRegister(false);
      }
    } catch (err) {
      alert("Ошибка авторизации/регистрации");
    }
  };

  return (
    <div className="flex items-center justify-center h-screen">
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow w-96 space-y-4">
        <h2 className="text-xl font-bold text-center">
          {isRegister ? "Регистрация" : "Вход"}
        </h2>
        <input
          type="text"
          placeholder="Логин"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full border p-2 rounded"
        />
        <input
          type="password"
          placeholder="Пароль"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full border p-2 rounded"
        />
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded"
        >
          {isRegister ? "Зарегистрироваться" : "Войти"}
        </button>
        <p className="text-sm text-center">
          {isRegister ? (
            <span>
              Уже есть аккаунт?{' '}
              <button
                type="button"
                onClick={() => setIsRegister(false)}
                className="text-blue-600"
              >
                Войти
              </button>
            </span>
          ) : (
            <span>
              Нет аккаунта?{' '}
              <button
                type="button"
                onClick={() => setIsRegister(true)}
                className="text-blue-600"
              >
                Зарегистрироваться
              </button>
            </span>
          )}
        </p>
      </form>
    </div>
  );
}
