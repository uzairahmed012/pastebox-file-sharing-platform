import axios from "axios";

const BASE_URL="http://localhost:6600/api/"
const axiosInstance=axios.create({
  baseURL: BASE_URL,
  withCredentials: true
});

// Don't set Content-Type header globally - let axios handle it automatically for FormData

export default axiosInstance;