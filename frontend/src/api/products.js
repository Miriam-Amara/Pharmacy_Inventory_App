import axios from "axios";

import { showToast } from "../utils/toast";


export async function addProductApi(productData) {
  try{
    let response = await axios.post("/api/v1/products", productData);
    return response.data
  }
  catch (error) {
    if (error.response)
      showToast(error?.response?.data?.error || "Error adding product", "error");
    else
      console.error("error: ", error);
  }
}

export async function updateProductApi(productData, product_id) {
  try{
    let response = await axios.put(
      `/api/v1/products/${product_id}`,
      productData,
      {withCredentials: true}
    );
    return response.data
  }
  catch (error) {
    if (error.response)
      showToast(error?.response?.data?.error || "Error updating product", "error");
    else
      console.error("error: ", error);
  }
}

export async function fetchProductApi(product_id) {
  try{
    let response = await axios.get(
      `api/v1/products/${product_id}`,
      {withCredentials: true}
    )    
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
  }
}

export async function fetchAllProductsApi(pageSize, pageNum, search) {
  try{
    pageSize = pageSize || 5
    pageNum = pageNum || 1

    let response = await axios.get(
      `api/v1/products/${pageSize}/${pageNum}`,
      {
        withCredentials: true,
        params: {search: search || ""}
      }
  )
    return response.data;
  }
  catch (error) {
    if (error.response) {
      showToast(
      error?.response?.data?.error ||
      "Error fetching products. Please contact admin.", "error"
    );}
    else
      console.error("error: ", error);
  }
}

export async function deleteProductApi(product_id) {
  try{
    await axios.delete(
      `api/v1/products/${product_id}`,
      {withCredentials: true}
    )
  }
  catch (error) {
    if (error.response) {
      showToast(
      error?.response?.data?.error ||
      "Error deleting product. Please contact admin.", "error"
    );}
    else
      console.error("error: ", error); 
  }
}

export async function fetchFilteredProductsByBrandAndCategory(
  brand_id, category_id, pageSize, pageNum) {
  try {
    if (brand_id && category_id) {
      var response = await axios.get(
      `api/v1/categories/${category_id}/brands/${brand_id}/products/${pageSize}/${pageNum}`,
      {withCredentials: true}
    )}
    else if (brand_id) {
      response = await axios.get(
      `api/v1/brands/${brand_id}/products/${pageSize}/${pageNum}`,
      {withCredentials: true}
    )}
    else{
      response = await axios.get(
      `api/v1/categories/${category_id}/products/${pageSize}/${pageNum}`,
      {withCredentials: true}
    )}
    
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
  }
}
