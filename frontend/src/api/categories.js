import api from "./api";
import { showToast } from "../utils/toast";


export async function addCategoryApi(categoryData) {
  try{
    let response = await api.post("/categories", categoryData);
    return response.data
  }
  catch (error) {
    if (error.response)
      showToast(error?.response?.data?.error || "Error adding category", "error");
    else {
      console.error(error);
      throw error;
    }
  }
}

export async function updateCategoryApi(categoryData, category_id) {
  try{
    let response = await api.put(`/categories/${category_id}`, categoryData);
    return response.data
  }
  catch (error) {
    if (error.response)
      showToast(error?.response?.data?.error || "Error updating category", "error");
    else {
      console.error(error);
      throw error;
    }
  }
}

export async function fetchCategoryApi(category_id) {
  try{
    let response = await api.get(`/categories/${category_id}`);
    return response.data;
  }
  catch (error) {
    if (error.response) {
      showToast(
      error?.response?.data?.error ||
      "Error fetching category. Please contact admin.", "error"
    );}
    else {
      console.error(error);
      throw error;
    }
  }
}

export async function fetchAllCategoriesApi(pageSize, pageNum, search) {
  try{
    pageSize = pageSize ?? 5
    pageNum = pageNum ?? 1

    let response = await api.get(
      `/categories/${pageSize}/${pageNum}`,
      {params: {search: search || ""}}
  );
    return response.data;
  }
  catch (error) {
    if (error.response)
      console.log("error in fetchAllCategoriesApi: ", error.response.data.error)
    else {
      console.error(error);
      throw error;
    }
  }
}

export async function deleteCategoryApi(category_id) {
  try{
    await api.delete(`/categories/${category_id}`);
  }
  catch (error) {
    if (error.response) {
      showToast(
      error?.response?.data?.error ||
      "Error deleting category. Please contact admin.", "error"
    );}
    else {
      console.error(error);
      throw error;
    }
  }
}
