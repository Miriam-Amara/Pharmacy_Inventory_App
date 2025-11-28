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
import {
  DisplayProductFormModal,
  DisplayProductsTable,
  DisplayProductsReorderingPoint,
  DisplayProductsGrid,
  DisplayProductDetailsModal
} from "../../components/ProductDisplay";


export default function ProductPage() {
  const {
    formData,
    errors,
    brand,
    brands,
    category,
    categories,
    products,
    mode, setMode,
    showForm, setShowForm,
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
      <main className="content-container">

        {/* Title Section */}
        <section className="title-section">
          <h5>Products</h5>
          <p>Add, delete, edit and view products.</p>
        </section>


        {/* Control Section */}
        <section className="control-section">
          <div className="add">
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

          <div className="pagination">
            <Pagination pageSize={pageSize} setPageSize={setPageSize} />
          </div>
          
          <div className="filter">
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
          </div>

          <div className="search">
            <SearchProduct search={search} setSearch={setSearch} />
          </div>
        </section>


        {/* Display Section */}
        <section className="display-section">
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
            Table
          </button>

          <button
            type="button"
            onClick={() => {setDisplayType("reordering point")}}
          >
            Reordering Point
          </button>

          <button
            type="button"
            onClick={() => {setDisplayType("grid")}}
          >
            Grid View
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