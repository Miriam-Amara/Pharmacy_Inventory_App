import api from "./api";
import { showToast } from "../utils/toast";


export async function addProductApi(productData) {
  try{
    let response = await api.post("/products", productData);
    return response.data
  }
  catch (error) {
    console.log("Error in addProductApi: ", error.response.data.error)
    if (error.response)
      showToast(error?.response?.data?.error || "Error adding product", "error");
    else
      console.error("error: ", error);
    throw error;
  }
}

export async function updateProductApi(productData, product_id) {
  try{
    let response = await api.put(`/products/${product_id}`, productData);
    return response.data
  }
  catch (error) {
    if (error.response)
      showToast(error?.response?.data?.error || "Error updating product", "error");
    else
      console.error("error: ", error);
    throw error;
  }
}

export async function fetchProductApi(product_id) {
  try{
    let response = await api.get(`/products/${product_id}`)
    return response.data;
  }
  catch (error) {
    if (error.response) {
      showToast(
      error?.response?.data?.error ||
      "Error fetching product. Please contact admin.", "error"
    );}
    else
      console.error("error: ", error);
    throw error;
  }
}

export async function fetchAllProductsApi(pageSize, pageNum, search) {
  try{
    pageSize = pageSize || 5
    pageNum = pageNum || 1

    let response = await api.get(
      `/products/${pageSize}/${pageNum}`,
      {params: {search: search || null}}
  )
    return response.data;
  }
  catch (error) {
    if (error.response) {
      console.log("error in fetchAllProductsApi: ", error.response.data.error)
    }
    else
      console.error("error: ", error);
    throw error;
  }
}

export async function deleteProductApi(product_id) {
  try{
    await api.delete(`/products/${product_id}`)
  }
  catch (error) {
    if (error.response) {
      showToast(
      error?.response?.data?.error ||
      "Error deleting product. Please contact admin.", "error"
    );}
    else
      console.error("error: ", error);
    throw error;
  }
}

export async function fetchFilteredProductsByBrandAndCategory(
  brand_id, category_id, pageSize, pageNum) {
  try {
    if (brand_id && category_id) {
      var response = await api.get(
      `/categories/${category_id}/brands/${brand_id}/products/${pageSize}/${pageNum}`,
    )}
    else if (brand_id) {
      response = await api.get(`/brands/${brand_id}/products/${pageSize}/${pageNum}`)}
    else{
      response = await api.get(`/categories/${category_id}/products/${pageSize}/${pageNum}`)}
    return response.data;
  }
  catch (error) {
    if (error.response) {
      showToast(
      error?.response?.data?.error ||
      "Error fetching filtered products. Please contact admin.", "error"
    );}
    else
      console.error("error: ", error);
    throw error;
  }
}
