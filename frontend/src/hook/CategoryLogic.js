/* */

import { useState, useEffect } from "react";

import { categoryValidationSchema } from "../utils/formInputValidation";
import {
  addCategoryApi,
  fetchCategoryApi,
  fetchAllCategoriesApi,
  updateCategoryApi,
  deleteCategoryApi,
} from "../api/categories";
import { showToast } from "../utils/toast";



export default function useCategoryLogic () {
  const [formData, setFormData] = useState({name: "", description: ""});
  const [errors, setErrors] = useState({});
  const [mode, setMode] = useState("add");
  const [showForm, SetShowForm] = useState(false);

  const [pageSize, setPageSize] = useState(5);
  const [pageNum, setPageNum] = useState(1);

  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);

  const [search, setSearch] = useState("");

  const fetchAllCategories = async () => {
    const allCategories = await fetchAllCategoriesApi(pageSize, pageNum, search);
    setCategories(Array.isArray(allCategories) ? allCategories : []);
  }

  useEffect(() => {
    const timeout = setTimeout(() => {
      fetchAllCategories();
    }, 500); // call api after 0.5 seconds of no typing
    return () => clearTimeout(timeout);
  }, [pageSize, pageNum, search]
  );
  
  const resetForm = () => {
    setFormData({name: "", description: ""});
    setErrors({});
    setMode("add");
    SetShowForm(false);
  };

  const handleChange = (e) => {
    const {name, value} = e.target
    setFormData((prev) => ({...prev, [name]: value}));
  };

  /*
    - on form submit makes either post or put request.
    - resets form
    - fetches all categories
  */
  const handleSubmit= async (e) => {
    e.preventDefault();
    try{
      await categoryValidationSchema.validate(formData, {abortEarly: false});

      if (mode == "add") {
        const category_response = await addCategoryApi(formData);
        category_response && showToast(`${formData.name} added successfuly.`, "success");
      }
      else if (mode == "edit") {
        const category_response = await updateCategoryApi(formData, formData.id);
        category_response && showToast(`${formData.name} updated successfuly.`, "success");
      }

      setFormData({name: "", description: ""});
      setErrors({});
      setMode("add");
      fetchAllCategories();
    }
    catch (error) {
      console.error("Error in handle submit", error);
      if (error.inner) {
        const newError = {}
        for (const err of error.inner)
          newError[err.path] = err.message
        setErrors(newError);
      }
    }
  }

  // fetches fresh category details and sets formData with the details.
  const handleEdit = async (category) => {
    setMode("edit");
    SetShowForm(true);

    const fresh_category = await fetchCategoryApi(category.id)
    fresh_category && setFormData(fresh_category);

  };

  // makes delete request and refreshes category list.
  const handleDelete = async (category) => {
    if (!window.confirm(`Are you sure you want to delete ${category.name}?`))
      return;

    await deleteCategoryApi(category.id)
    fetchAllCategories();
  };

  // displays full category details
  const handleViewDetails = async (category) => {setSelectedCategory(category)};

  return ({
    formData, setFormData,
    errors, setErrors,
    mode, setMode,
    showForm, SetShowForm,
    pageSize, setPageSize,
    pageNum, setPageNum,
    categories, setCategories,
    selectedCategory, setSelectedCategory,
    search, setSearch,
    resetForm, handleChange, handleSubmit,
    handleEdit, handleDelete, handleViewDetails,
  });
};
