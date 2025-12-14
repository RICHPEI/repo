// Authentication service 處理 JWT token 和本地存儲

const TOKEN_KEY = 'auth_token';
const USER_KEY = 'user_data';

interface LoginCredentials {
  email: string;
  password: string;
  rememberMe: boolean;
}

interface AuthResponse {
  token: string;
  user: {
    id: string;
    email: string;
    name?: string;
  };
}

interface AuthError {
  message: string;
  code?: string;
}

/**
 * 登入 API 呼叫
 */
export async function login(credentials: LoginCredentials): Promise<AuthResponse> {
  try {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: credentials.email,
        password: credentials.password,
      }),
    });

    if (!response.ok) {
      const error: AuthError = await response.json();
      throw new Error(error.message || '登入失敗');
    }

    const data: AuthResponse = await response.json();

    // 儲存 token 和用戶資料
    saveAuthData(data, credentials.rememberMe);

    return data;
  } catch (error) {
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('網路連線錯誤，請稍後再試');
  }
}

/**
 * 儲存認證資料到 localStorage 或 sessionStorage
 */
function saveAuthData(data: AuthResponse, rememberMe: boolean) {
  const storage = rememberMe ? localStorage : sessionStorage;

  storage.setItem(TOKEN_KEY, data.token);
  storage.setItem(USER_KEY, JSON.stringify(data.user));
}

/**
 * 取得儲存的 token
 */
export function getToken(): string | null {
  // 優先從 localStorage 檢查，然後是 sessionStorage
  return localStorage.getItem(TOKEN_KEY) || sessionStorage.getItem(TOKEN_KEY);
}

/**
 * 取得儲存的用戶資料
 */
export function getUserData(): AuthResponse['user'] | null {
  const userJson = localStorage.getItem(USER_KEY) || sessionStorage.getItem(USER_KEY);
  if (!userJson) return null;

  try {
    return JSON.parse(userJson);
  } catch {
    return null;
  }
}

/**
 * 驗證 token 是否有效
 */
export function verifyToken(token: string): boolean {
  try {
    // JWT token 格式: header.payload.signature
    const parts = token.split('.');
    if (parts.length !== 3) return false;

    // 解碼 payload (base64)
    const payload = JSON.parse(atob(parts[1]));

    // 檢查是否過期
    if (payload.exp) {
      const expirationTime = payload.exp * 1000; // 轉換為毫秒
      return Date.now() < expirationTime;
    }

    return true;
  } catch {
    return false;
  }
}

/**
 * 檢查用戶是否已登入
 */
export function isAuthenticated(): boolean {
  const token = getToken();
  return token !== null && verifyToken(token);
}

/**
 * 登出
 */
export function logout() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
  sessionStorage.removeItem(TOKEN_KEY);
  sessionStorage.removeItem(USER_KEY);
}

/**
 * 在 API 請求中加入 Authorization header
 */
export function getAuthHeaders(): HeadersInit {
  const token = getToken();
  if (!token) return {};

  return {
    'Authorization': `Bearer ${token}`,
  };
}
