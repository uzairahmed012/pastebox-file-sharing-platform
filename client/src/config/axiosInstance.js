import axios from "axios";

// Using a relative URL so it works seamlessly on any domain (like AWS)
const axiosInstance = axios.create({
  baseURL: "/api",
  withCredentials: true
});

// Don't set Content-Type header globally - let axios handle it automatically for FormData

export default axiosInstance;