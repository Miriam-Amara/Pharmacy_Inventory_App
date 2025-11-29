import axios from "axios";

const apiUrl = import.meta.env.VITE_API_URL;

const api = axios.create({
  baseURL: apiUrl + "/api/v1",
  withCredentials: true, // important for session cookies
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    // If backend returns 401 → session expired
    if (error.response && error.response.status === 401) {
      window.location.href = "/login"; // redirect user to login page
    }
    return Promise.reject(error);
  }
);

export default api;
