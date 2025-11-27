/* */

import Layout from "../../components/Layout";
import useCategoryLogic from "../../hook/CategoryLogic"
import {
  AddCategory,
  Pagination,
  SearchCategory,
} from "../../components/CategoryControls";
import {
  DisplayCategoryFormModal,
  DisplayCategoriesTable,
  DisplayCategoryDetailsModal,
} from "../../components/CategoryDisplay";

import "../pages.css"


function CategoryPage() {
  const {
    formData, errors,
    mode, setMode,
    showForm, setShowForm,
    pageSize, setPageSize,
    // pageNum, setPageNum,
    categories,
    selectedCategory, setSelectedCategory,
    search, setSearch,
    resetForm, handleChange, handleSubmit,
    handleEdit, handleDelete, handleViewDetails,
  } = useCategoryLogic();
  
  return (
    <Layout
      main={
      <main className="content-container">
        
        {/* Title Section */}
        <section className="title-section">
          <h5>Categories</h5>
          <p>Add, delete, edit and view categories.</p>
        </section>

        {/* Control Section */}
        <section className="control-section">
          <div className="add">
            <AddCategory setMode={setMode} setShowForm={setShowForm} />

            {showForm && <DisplayCategoryFormModal 
              formData={formData}
              errors={errors}
              mode={mode}
              handleChange={handleChange}
              handleSubmit={handleSubmit}
              resetForm={resetForm}
            />}
          </div>

          <div className="pagination">
            <Pagination pageSize={pageSize} setPageSize={setPageSize} />
          </div>

          <div className="search">
            <SearchCategory search={search} setSearch={setSearch} />
          </div>
        </section>


        {/* Display Section */}
        <section className="display-section">
          {
            selectedCategory && <DisplayCategoryDetailsModal
              category={selectedCategory}
              setSelectedCategory={setSelectedCategory}
            />
          }

          {
            categories.length === 0 ? <p>No category found.</p> : <DisplayCategoriesTable
            categories={categories}
            handleViewDetails={handleViewDetails}
            handleEdit={handleEdit}
            handleDelete={handleDelete}
          />
          }
        </section>
      </main>
    }/>
  );
}

export default CategoryPage;
