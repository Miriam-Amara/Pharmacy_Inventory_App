import axios from "axios";

import { showToast } from "../utils/toast";


export async function addBrandApi(brand_data) {
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

export async function updateBrandApi(brand_id, data) {
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

export async function fetchBrandApi(brand_id) {
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

export async function fetchAllBrandsApi(pageSize, pageNum) {
  try{
    pageSize = pageSize ?? 5
    pageNum = pageNum ?? 1

    const response = await axios.get(
      `/api/v1/brands/${pageSize}/${pageNum}`,
      {withCredentials: true}
    );
    return response.data;
  }
  catch (error) {
    if (error.response)
      console.log("error in fetchAllBrandsApi: ", error.response.data.error)
    else
      console.error(error);
  }
}

export async function deleteBrandApi(brand_id) {
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
