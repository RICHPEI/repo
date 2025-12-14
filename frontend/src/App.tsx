import { useState, useEffect } from 'react';
import LoginForm from './components/LoginForm';
import { login, logout, isAuthenticated, getUserData } from './services/auth';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [loginError, setLoginError] = useState<string | undefined>();
  const [user, setUser] = useState<{ id: string; email: string; name?: string } | null>(null);

  // 檢查用戶是否已登入
  useEffect(() => {
    if (isAuthenticated()) {
      setIsLoggedIn(true);
      setUser(getUserData());
    }
  }, []);

  const handleLogin = async (formData: { email: string; password: string; rememberMe: boolean }) => {
    try {
      setLoginError(undefined);
      const response = await login(formData);
      setIsLoggedIn(true);
      setUser(response.user);
    } catch (error) {
      if (error instanceof Error) {
        setLoginError(error.message);
      } else {
        setLoginError('登入時發生未知錯誤');
      }
      throw error; // 讓 LoginForm 知道登入失敗
    }
  };

  const handleLogout = () => {
    logout();
    setIsLoggedIn(false);
    setUser(null);
  };

  if (!isLoggedIn) {
    return <LoginForm onSubmit={handleLogin} error={loginError} />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-2xl shadow-2xl p-8">
          <div className="flex justify-between items-center mb-8">
            <div>
              <h1 className="text-3xl font-bold text-gray-800">Excel 資料清洗工具</h1>
              <p className="text-gray-600 mt-2">歡迎回來，{user?.name || user?.email}！</p>
            </div>
            <button
              onClick={handleLogout}
              className="px-6 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition duration-200"
            >
              登出
            </button>
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">功能說明</h2>
            <ul className="space-y-2 text-gray-700">
              <li className="flex items-start">
                <span className="text-blue-600 mr-2">✓</span>
                <span>移除 Excel 檔案中的重複記錄</span>
              </li>
              <li className="flex items-start">
                <span className="text-blue-600 mr-2">✓</span>
                <span>支援自訂欄位進行重複檢測</span>
              </li>
              <li className="flex items-start">
                <span className="text-blue-600 mr-2">✓</span>
                <span>完整的日誌記錄系統</span>
              </li>
              <li className="flex items-start">
                <span className="text-blue-600 mr-2">✓</span>
                <span>單元測試覆蓋率完整</span>
              </li>
            </ul>
          </div>

          <div className="mt-6 p-4 bg-gray-50 rounded-lg">
            <p className="text-sm text-gray-600 text-center">
              這是一個示例頁面。未來可以在這裡添加檔案上傳和處理功能。
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
