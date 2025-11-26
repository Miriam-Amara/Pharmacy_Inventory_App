import axios from "axios";

import { showToast } from "../utils/toast";


export async function addCategoryApi(categoryData) {
  try{
    let response = await axios.post("/api/v1/categories", categoryData);
    return response.data
  }
  catch (error) {
    if (error.response)
      showToast(error?.response?.data?.error || "Error adding category", "error");
    else
      console.error("error: ", error);
  }
}

export async function updateCategoryApi(categoryData, category_id) {
  try{
    let response = await axios.put(
      `/api/v1/categories/${category_id}`,
      categoryData,
      {withCredentials: true}
    );
    return response.data
  }
  catch (error) {
    if (error.response)
      showToast(error?.response?.data?.error || "Error updating category", "error");
    else
      console.error("error: ", error);
  }
}

export async function fetchCategoryApi(category_id) {
  try{
    let response = await axios.get(
      `api/v1/categories/${category_id}`,
      {withCredentials: true}
    )    
    return response.data;
  }
  catch (error) {
    if (error.response) {
      showToast(
      error?.response?.data?.error ||
      "Error fetching category. Please contact admin.", "error"
    );}
    else
      console.error("error: ", error);
  }
}

export async function fetchAllCategoriesApi(pageSize, pageNum, search) {
  try{
    pageSize = pageSize ?? 5
    pageNum = pageNum ?? 1

    let response = await axios.get(
      `api/v1/categories/${pageSize}/${pageNum}`,
      {
        withCredentials: true,
        params: {search: search || ""}
      }
  )
    return response.data;
  }
  catch (error) {
    if (error.response)
      console.log("error in fetchAllCategoriesApi: ", error.response.data.error)
    else
      console.error("error: ", error);
  }
}

export async function deleteCategoryApi(category_id) {
  try{
    await axios.delete(
      `api/v1/categories/${category_id}`,
      {withCredentials: true}
    )
  }
  catch (error) {
    if (error.response) {
      showToast(
      error?.response?.data?.error ||
      "Error deleting category. Please contact admin.", "error"
    );}
    else
      console.error("error: ", error); 
  }
}