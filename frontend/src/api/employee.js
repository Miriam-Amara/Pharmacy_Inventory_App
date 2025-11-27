import api from "./api";
import { showToast } from "../utils/toast";


export async function registerApi(registerData) {
  try{
    await api.post("/register", registerData);
  }
  catch (error) {
    showToast(error.response?.data?.error, "error");
  }
}

export async function loginApi(loginData) {
  try{
    const response = await api.post("/auth_session/login", loginData);
    return (response);
  }
  catch (error) {
    showToast(error.response?.data?.error, "error");
    throw error;
  }
}

export async function updateEmployeeApi(employee_id, data) {
  try{
    await api.put(`/employees/${employee_id}`, data);
    showToast("Profile updated successfully", "success");
  }
  catch (error) {
    showToast(error.response?.data?.error || "Error updating profile.", "error");
  }
}

export async function fetchMe() {
  try{
    const response = await api.get("/employees/me");
    return response.data;
  }
  catch (error) {
    console.error(
      error.response?.data?.error || "Error fetching employee profile."
    );
    throw error;
  }
}

export async function fetchEmployeeApi(employee_id) {
  try{
    const response = await api.get(`/employees/${employee_id}`);
    return response.data;
  }
  catch (error) {
    console.error(error.response?.data?.error || "Error fetching employee profile.");
    throw error;
  }
}

export async function fetchAllEmployeesApi() {
  try{
    const response = await api.get(`/employees/${50}/${1}`);
    return response.data;
  }
  catch (error) {
    showToast(error.response?.data?.error || "Error fetching employees", "error");
    throw error;
  }
}
