import axios from "axios";

// ✅ Create axios instance
const api = axios.create({
  baseURL: "http://localhost:5000/api",
  headers: { "Content-Type": "application/json" },
  withCredentials: true, // ✅ include cookies if backend uses sessions
});

// ✅ Interceptor to automatically attach JWT token if stored
api.interceptors.request.use((config) => {
  const stored = localStorage.getItem("smartLaundryUser");
  if (stored) {
    const { token } = JSON.parse(stored);
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
  }
  return config;
}, (error) => Promise.reject(error));

// Contact form submit
export const sendContactForm = async (formData) => {
  const res = await api.post("/contact/submit", formData);
  return res.data;
};

export default api;
