/* */

import { useState, useEffect } from "react";

import { showToast } from "../utils/toast";
import { productValidationSchema } from "../utils/formInputValidation";
import { fetchAllBrandsApi } from "../api/brands";
import { fetchAllCategoriesApi } from "../api/categories";
import {
  addProductApi,
  fetchProductApi,
  fetchAllProductsApi,
  updateProductApi,
  fetchFilteredProductsByBrandAndCategory,
  deleteProductApi,
} from "../api/products";



export default function useProductLogic() {
  const [formData, setFormData] = useState({
    barcode: "",
    name: "",
    unit_cost_price: "",
    unit_selling_price: "",
    category_id: "",
    brand_id: "",
    brand_name: "",
    created_at: "",
    last_updated: "",
  });
  const [errors, setErrors] = useState({});
  const [mode, setMode] = useState("add");
  const [showForm, setShowForm] = useState(false);

  const [brand, setBrand] = useState({brand_id: ""});
  const [brands, setBrands] = useState([]);
  const [category, setCategory] = useState({category_id: ""});
  const [categories, setCategories] = useState([]);
  const [products, setProducts] = useState([]);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [pageSize, setPageSize] = useState(5);
  const [pageNum, setPageNum] = useState(1);
  const [search, setSearch] = useState("");

  const [displayType, setDisplayType] = useState("table");


  const fetchAllProducts = async () => {
    const allProducts = await fetchAllProductsApi(pageSize, pageNum, search);
    setProducts(allProducts ?? []);
  };

  useEffect(() => {
    const fetchData = async () => {
      if (search.trim() !== "") {
        await fetchAllProducts();
      }
      else if (brand.brand_id !== "" || category.category_id !== "") {
        const filteredProducts = await fetchFilteredProductsByBrandAndCategory(
            brand.brand_id,
            category.category_id,
            pageSize,
            pageNum
          );
          setProducts(filteredProducts ?? [])
      }
      else {
        await fetchAllProducts();
      }
    }

    const timeout = setTimeout(() => {
      fetchData();
    }, 500)
    return () => clearTimeout(timeout);
  }, [brand.brand_id, category.category_id, pageSize, pageNum, search]
  );

  const resetForm = () => {
    setFormData({
      barcode: "",
      name: "",
      unit_cost_price: "",
      unit_selling_price: "",
      category_id: "",
      brand_id: "",
      brand_name: "",
      created_at: "",
      last_updated: "",
    });
    setErrors({});
    setMode("add");
  };

  const handleChange = (e) => {
    const {name, value} = e.target
    setFormData((prev) => (
      {
        ...prev,
        [name]: value,
        ...(name === "brand_id" && value !== "" ? { brand_name: "" } : {})
      }))
  };

  // handle submit for both add and update product events
  // validates formData, makes post or put request and resets form
  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const validData = await productValidationSchema.validate(
        formData, {abortEarly: false}
      )

      if (mode === "add") {
        const productResponse = await addProductApi(validData);
        productResponse && showToast(`${formData.name} added successfully`, "success");
      }
      else if (mode === "edit") {
        const productResponse = await updateProductApi(validData, validData.id);
        productResponse && showToast(`${formData.name} added successfully`, "success");
      }
      fetchAllProducts();
      resetForm();
    }
    catch (error) {
      console.error("Error in handleSubmit: ", error.inner)
      if (error.inner) {
        const newError = {}
        for (const err of error.inner)
          newError[err.path] = err.message
        setErrors(newError);
      }
    }
  };

  const handleViewDetails = (product) => {setSelectedProduct(product);};

  const handleEdit = async (product) => {
    setMode("edit");
    setShowForm(true);

    const fresh_product = await fetchProductApi(product.id);
    setFormData(fresh_product);
  };

  const handleDelete = async (product) => {
    if (!window.confirm(`Are you sure you want to delete ${product.name}?`))
      return;
    await deleteProductApi(product.id);
    fetchAllProducts();
  };

  const handleFetchBrands = async () => {
    const allBrands = await fetchAllBrandsApi(0, 0);
    if (Array.isArray(allBrands)) {
      const sortedBrands = allBrands.sort(
        (a, b) => a.name.localeCompare(b.name)
      );
      setBrands(sortedBrands);
    }
    else {
      setBrands([]);
    }
  }

  const handleFetchCategories = async () => {
    const allCategories = await fetchAllCategoriesApi(0, 0);
    if (Array.isArray(allCategories)) {
      const sortedCategories = allCategories.sort(
        (a, b) => a.name.localeCompare(b.name)
      );
      setCategories(sortedCategories);
    }
    else {
      setCategories([]);
    }
  }

  const handleFetchFilteredProducts = (e, type) => {
    const {name, value} = e.target
    
    if (type === "brand")
      setBrand({[name]: value})
    else if (type === "category")
      setCategory({[name]: value})
  }

  return ({
    formData, setFormData,
    errors, setErrors,
    mode, setMode,
    showForm, setShowForm,
    brand, setBrand,
    brands, setBrands,
    category, setCategory,
    categories, setCategories,
    products, setProducts,
    selectedProduct, setSelectedProduct,
    pageSize, setPageSize,
    pageNum, setPageNum,
    search, setSearch,
    displayType, setDisplayType,
    resetForm, handleChange, handleSubmit,
    handleViewDetails, handleEdit, handleDelete,
    handleFetchBrands, handleFetchCategories,
    handleFetchFilteredProducts,
  });
}
