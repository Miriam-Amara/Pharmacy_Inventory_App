import axios from "axios";


export async function addCategoryApi(categoryData) {
  try{
    let response = await axios.post("/api/v1/categories", categoryData);
    console.log(response.status);
    console.log(response.data);
    return response.data
  }
  catch (error) {
    console.log(error.response.status);
    console.log(error.response.data);
  }
}

export async function updateCategoryApi(categoryData, category_id) {
  try{
    let response = await axios.put(
      `/api/v1/categories/${category_id}`,
      categoryData,
      {withCredentials: true}
    );
    console.log(response.status);
    console.log(response.data);
    return response.data
  }
  catch (error) {
    console.log(error.response.status);
    console.log(error.response.data);
  }
}

export async function fetchCategoryApi(category_id) {
  try{
    let response = await axios.get(
      `api/v1/categories/${category_id}`,
      {withCredentials: true}
    )
    console.log(response.status);
    console.log(response.data);
    return response.data;
  }
  catch (error) {
    console.log(error.response.status);
    console.log(error.response.data);
  }
}

export async function fetchAllCategoriesApi(pageSize, pageNum, search) {
  try{
    pageSize = pageSize || 5
    pageNum = pageNum || 1

    let response = await axios.get(
      `api/v1/categories/${pageSize}/${pageNum}`,
      {
        withCredentials: true,
        params: {search: search || ""}
      }
  )
    console.log(response.status);
    console.log(response.data);
    return response.data;
  }
  catch (error) {
    console.log(error.response.status);
    console.log(error.response.data);
  }
}

export async function deleteCategoryApi(category_id) {
  try{
    let response = await axios.delete(
      `api/v1/categories/${category_id}`,
      {withCredentials: true}
    )
    console.log(response.status);
    console.log(response.data);
  }
  catch (error) {
    console.log(error.response.status);
    console.log(error.response.data);
  }
}