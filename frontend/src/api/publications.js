import axios from "axios";

const api = axios.create({
  baseURL: "/api",
});

// Токен хранится в памяти на время сессии
let authToken = null;

export function setToken(token) {
  authToken = token;
  api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
}

export function getToken() {
  return authToken;
}

export function clearToken() {
  authToken = null;
  delete api.defaults.headers.common["Authorization"];
}

// --- Users ---

export async function createUser(name) {
  const { data } = await api.post("/users", { name });
  setToken(data.access_token);
  return data;
}

// --- Publications ---

export async function fetchPublications({ limit = 20, offset = 0, userId = null } = {}) {
  const params = { limit, offset };
  if (userId) params.user_id = userId;

  const { data } = await api.get("/publications", { params });
  return data;
}

export async function fetchPublication(id) {
  const { data } = await api.get(`/publications/${id}`);
  return data;
}

export async function createPublication(title, text) {
  const { data } = await api.post("/publications", { title, text });
  return data;
}
