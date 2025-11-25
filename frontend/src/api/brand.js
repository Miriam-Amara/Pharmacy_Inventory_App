import axios from "axios";

import { showToast } from "../utils/toast";


export async function addBrand(brand_data) {
  try{
    await axios.post(
      "/api/v1/brands",
      brand_data,
      {withCredentials: true}
    );
  }
  catch (error) {
    if (error.response)
      showToast(error?.response?.data?.error || "Error adding brand", "error");
    else
      console.error(error);
  }
}

export async function updateBrand(brand_id, data) {
  try{
    await axios.put(
      `/api/v1/brands/${brand_id}`,
      data,
      {withCredentials: true}
    );
  }
  catch (error) {
    if (error.response)
      showToast(error?.response?.data?.error || "Error updating brand", "eror");
    else
      console.error(error);
  }
}

export async function getBrand(brand_id) {
  try{
    const response = await axios.get(
      `/api/v1/brands/${brand_id}`,
      {withCredentials: true}
    );
    return response.data;
  }
  catch (error) {
    if (error.response)
      showToast(error?.response?.data?.error || "Error getting the brand", "error")
    else
      console.error(error);
  }
}

export async function getAllBrands(page_size, page_num) {
  try{
    const response = await axios.get(
      `/api/v1/brands/${page_size}/${page_num}`,
      {withCredentials: true}
    );
    return response.data;
  }
  catch (error) {
    if (error.response)
      showToast(error?.response?.data?.error || "Error getting brands", "error");
    else
      console.error(error);
  }
}

export async function deleteBrand(brand_id) {
  try{
    await axios.delete(
      `/api/v1/brands/${brand_id}`,
      {withCredentials: true}
    );
  }
  catch (error) {
    if (error.response)
      showToast(error?.response?.data?.error || "Error deleting brand", "error");
    else
      console.error(error);
  }
}
