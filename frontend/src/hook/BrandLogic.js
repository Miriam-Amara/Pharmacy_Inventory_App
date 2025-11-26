/* */

import { useState, useEffect } from "react";

import { brandValidationSchema } from "../utils/formInputValidation";
import {
  addBrandApi,
  fetchBrandApi,
  fetchAllBrandsApi,
  updateBrandApi,
  deleteBrandApi,
} from "../api/brands";
import { showToast } from "../utils/toast";


function useBrandLogic() {
  const [formData, setFormData] = useState({name: "", is_active: true})
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [brands, setBrands] = useState([]);
  const [filteredBrands, setFilteredBrands] = useState([]);
  const [query, setQuery] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [formMode, setFormMode] = useState("add");
  const [pageSize, setPageSize] = useState(10);
  const [pageNum, setPageNum] = useState(1);
  const [pageSizeInput, setPageSizeInput] = useState(pageSize);
  const [pageNumInput, setPageNumInput] = useState(pageNum);
  const [selectedBrand, setSelectedBrand] = useState(null);
  const [search, setSearch] = useState(false);

  const fetchBrands = async () => {
    setLoading(true);
    const allBrands = await fetchAllBrandsApi(pageSize, pageNum);
    setBrands(Array.isArray(allBrands) ? allBrands : []);
    setLoading(false);
  };

  useEffect(() => {fetchBrands();}, [pageSize, pageNum]);

  useEffect(() => {
    if (!query.trim()){
      setFilteredBrands(brands);
      setSearch(false);
      return;
    }
    const filtered = brands.filter((b) =>
      b.name.toLowerCase().includes(query.toLowerCase())
    );
    setFilteredBrands(filtered);
    setSearch(true);
  }, [query, brands]);

  const resetForm = () => {
    setFormData({name: "", is_active: true});
    setErrors({});
    setFormMode("add");
    setShowForm(false);
  };

  const handleChange = (e) => {
    const {name, value} = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === "is_active" ? value === "true" : value
    }));
  };

  const handleDelete = async (brand) => {
    if (!window.confirm(`Are you sure you want to delete ${brand.name}?`))
      return;

    await deleteBrandApi(brand.id);
    await fetchBrands();
  };

  const handleEdit = async (brand) => {
    setFormMode("edit");
    setShowForm(true);
    const freshBrand = await fetchBrandApi(brand.id);
    setFormData(freshBrand);
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    try{
      await brandValidationSchema.validate(formData, {abortEarly: false})

      if (formMode === "add") {
        const brand_data = await addBrandApi(formData);
        brand_data && showToast(`${formData.name} added successfully`, "success")
      }
      else {
        await updateBrandApi(formData.id, formData);
        showToast(`${formData.name} updated successfully`, "success")
      }

      await fetchBrands();
      setFormData({name: "", is_active: true});
      setErrors({});
      setFormMode("add");
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
  };

  const handleViewDetails = (brand) => {setSelectedBrand(brand);};
  const closeDetailsModal = () => {setSelectedBrand(null);};

  return {
    brands,
    errors,
    filteredBrands,
    formData,
    formMode,
    loading,
    pageSize,
    pageNum,
    pageSizeInput,
    pageNumInput,
    query,
    selectedBrand,
    search,
    showForm,
    closeDetailsModal,
    setFormMode,
    setPageSize,
    setPageNum,
    setPageSizeInput,
    setPageNumInput,
    setQuery,
    setShowForm,
    handleChange,
    handleDelete,
    handleEdit,
    handleSubmit,
    handleViewDetails,
    resetForm,
  };
}

export default useBrandLogic;
