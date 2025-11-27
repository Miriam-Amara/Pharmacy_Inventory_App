import api from "./api";
import { showToast } from "../utils/toast";


export async function addBrandApi(brand_data) {
  try{
    await api.post("/brands", brand_data);
  }
  catch (error) {
    if (error.response)
      showToast(error?.response?.data?.error || "Error adding brand", "error");
    else {
      console.error(error);
      throw error;
    }
  }
}

export async function updateBrandApi(brand_id, data) {
  try{
    await api.put(`/brands/${brand_id}`, data);
  }
  catch (error) {
    if (error.response)
      showToast(error?.response?.data?.error || "Error updating brand", "eror");
    else {
      console.error(error);
      throw error;
    }
  }
}

export async function fetchBrandApi(brand_id) {
  try{
    const response = await api.get(`/brands/${brand_id}`);
    return response.data;
  }
  catch (error) {
    if (error.response)
      showToast(error?.response?.data?.error || "Error getting the brand", "error")
    else {
      console.error(error);
      throw error;
    }
  }
}

export async function fetchAllBrandsApi(pageSize, pageNum) {
  try{
    pageSize = pageSize ?? 5
    pageNum = pageNum ?? 1

    const response = await api.get(`/brands/${pageSize}/${pageNum}`);
    return response.data;
  }
  catch (error) {
    if (error.response)
      console.log("error in fetchAllBrandsApi: ", error.response.data.error)
    else {
      console.error(error);
      throw error;
    }
  }
}

export async function deleteBrandApi(brand_id) {
  try{
    await api.delete(`/brands/${brand_id}`);
  }
  catch (error) {
    if (error.response)
      showToast(error?.response?.data?.error || "Error deleting brand", "error");
    else {
      console.error(error);
      throw error;
    }
  }
}
