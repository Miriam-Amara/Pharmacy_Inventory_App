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



function CategoryPage() {
  const {
    formData, errors,
    mode, setMode,
    showForm, SetShowForm,
    pageSize, setPageSize,
    // pageNum, setPageNum,
    categories,
    selectedCategory, setSelectedCategory,
    search, setSearch,
    resetForm, handleChange, handleSubmit,
    handleEdit, handleDelete, handleViewDetails,
  } = useCategoryLogic();
  
  return (
    <Layout main={
    <main>
      
      {/* Title Section */}
      <section>
        <h3>Categories</h3>
        <p>Add, delete, edit and view categories</p>
      </section>

      {/* Control Section */}
      <section>
        <div>
          <AddCategory setMode={setMode} SetShowForm={SetShowForm} />
          {showForm && <DisplayCategoryFormModal 
            formData={formData}
            errors={errors}
            mode={mode}
            handleChange={handleChange}
            handleSubmit={handleSubmit}
            resetForm={resetForm}
          />}
        </div>

        <div>
          <Pagination pageSize={pageSize} setPageSize={setPageSize} />
        </div>

        <div>
          <SearchCategory search={search} setSearch={setSearch} />
        </div>
      </section>

      {/* Display Section */}
      <section>
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
