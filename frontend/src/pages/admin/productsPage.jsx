/* */

import useProductLogic from "../../hook/ProductLogic";
import Layout from "../../components/Layout";
import {
  AddProduct,
  FilterProductByCategory,
  FilterProductByBrand,
  SearchProduct,
  Pagination,
} from "../../components/ProductControls";


export default function ProductPage() {
  const {
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
    // pageNum, setPageNum,
    search, setSearch,
    displayType, setDisplayType,
    resetForm, handleChange, handleSubmit,
    handleViewDetails, handleEdit, handleDelete,
    handleFetchBrands, handleFetchCategories,
    handleFetchFilteredProducts,
  } = useProductLogic();

  return (
    <Layout main={
      <main>

        {/* Title Section */}
        <section>
          <h3>Products</h3>
          <p>Add, delete, edit and view products.</p>
        </section>


        {/* Control Section */}
        <section>
          <div>
            <AddProduct setMode={setMode} setShowForm={setShowForm} />
            {showForm && <DisplayProductFormModal 
              formData={formData}
              errors={errors}
              mode={mode}
              brands={brands}
              categories={categories}
              handleFetchBrands={handleFetchBrands}
              handleFetchCategories={handleFetchCategories}
              handleChange={handleChange}
              handleSubmit={handleSubmit}
              resetForm={resetForm}
              setShowForm={setShowForm}
            />}
          </div>
          
          <div>
            <FilterProductByCategory
              category={category}
              categories={categories}
              handleFetchCategories={handleFetchCategories}
              handleFetchFilteredProducts={handleFetchFilteredProducts}
            />
          </div>

          <div>
            <FilterProductByBrand
              brand={brand}
              brands={brands}
              handleFetchBrands={handleFetchBrands}
              handleFetchFilteredProducts={handleFetchFilteredProducts}
            />
          </div>

          <div>
            <SearchProduct search={search} setSearch={setSearch} />
          </div>

          <div>
            <Pagination pageSize={pageSize} setPageSize={setPageSize} />
          </div>
        </section>


        {/* Display Section */}
        <section>
          {
            selectedProduct && <DisplayProductDetailsModal
              product={selectedProduct}
              setSelectedProduct={setSelectedProduct}
            />
          }

          <button
            type="button"
            onClick={() => {setDisplayType("table")}}
          >
            Display Table
          </button>

          <button
            type="button"
            onClick={() => {setDisplayType("reordering point")}}
          >
            Display Reordering Point
          </button>

          <button
            type="button"
            onClick={() => {setDisplayType("grid")}}
          >
            Display Grid
          </button>

          {
            products.length === 0 ? <p>No product found. Please add products.</p>
            : displayType === "table" ? <DisplayProductsTable
                products={products}
                handleViewDetails={handleViewDetails}
                handleEdit={handleEdit}
                handleDelete={handleDelete}
              />
            : displayType === "reordering point" ? <DisplayProductsReorderingPoint
                products={products}
            />
            : <DisplayProductsGrid
                products={products}
              />
          }
        </section>

      </main>
    }
    />
  );
}