import axios from "axios";


export async function addProduct(productData){
  try{
    const response = await axios.post(
      "/api/v1/products", productData, {withCredentials: true}
    );
    console.log(response);
    // return response;
  }
  catch (error) {
    console.log(error.response.status)
    console.log(error.response.data)
  }
};
