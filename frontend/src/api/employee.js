import axios from "axios";

import { showToast } from "../utils/toast";


export async function register(registerData) {
  try{
    await axios.post("/api/v1/register", registerData);
  }
  catch (error) {
    showToast(error.response?.data?.error, "error");
  }
}

export async function login(loginData) {
  try{
    await axios.post("/api/v1/auth_session/login", loginData);
  }
  catch (error) {
    showToast(error.response?.data?.error, "error");
    throw error;
  }
}

export async function updateEmployee(employee_id, data) {
  try{
    await axios.put(`/api/v1/employees/${employee_id}`, data, {withCredentials: true});
    showToast("Profile updated successfully", "success");
  }
  catch (error) {
    showToast(error.response?.data?.error || "Error updating profile.", "error");
  }
}

export async function fetchMe() {
  try{
    const response = await axios.get("/api/v1/employees/me", {withCredentials: true});
    return response.data;
  }
  catch (error) {
    console.log(
      "Error in fetchMe(): ",
      error.response?.data?.error || "Error fetching employee profile."
    );
  }
}

export async function fetchEmployee(employee_id) {
  console.log("Employee id:", employee_id);
  try{
    const response = await axios.get(
      `/api/v1/employees/${employee_id}`,
      {withCredentials: true}
    );
    return response.data;
  }
  catch (error) {
    console.log(error.response?.data?.error || "Error fetching employee profile.");
  }
}

export async function fetchAllEmployees() {
  try{
    const response = await axios.get(
      `/api/v1/employees/${50}/${1}`,
      {withCredentials: true}
    );
    return response.data;
  }
  catch (error) {
    showToast(error.response?.data?.error || "Error fetching employees", "error");
  }
}
