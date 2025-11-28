/* */

import useBrandLogic from "../../hook/BrandLogic";
import BrandForm from "../../components/BrandForm";
import { BrandTable, BrandDetailsModal } from "../../components/BrandDisplay";
import Layout from "../../components/Layout";


function BrandPageView() {
  const {
    formData, errors,
    selectedBrand, search,
    loading, filteredBrands,
    formMode, setFormMode,
    pageSize, setPageSize,
    query, setQuery,
    showForm, setShowForm,
    closeDetailsModal, resetForm,
    handleChange, handleDelete, handleEdit,
    handleSubmit, handleViewDetails,
  } = useBrandLogic();

  return (
    <main className="content-container">

      {/* Info section */}
      <section className="title-section">
        <h5>Brands</h5>
        <p>View, add, edit and delete brands.</p>
      </section>

      {/* Control Section - forms, search, pagination */}
      <section className="control-section">

        {/* Form */}
        <div className="add">
          <button
            onClick={() => {setFormMode("add"); setShowForm(true);}}
          >
              Add Brand
          </button>

          {showForm && (
            <BrandForm
              formData={formData}
              errors={errors}
              formMode={formMode}
              handleChange={handleChange}
              handleSubmit={handleSubmit}
              resetForm={resetForm}
            />
          )}
        </div>

        {/* Pagination */}
        <div className="pagination">
          <p>Show</p>
          <input
            type="number"
            name="pageSize"
            value={pageSize}
            min={1}
            onChange={(e) => {
              const val = Number(e.target.value)
              setPageSize(val < 1 ? 1 : val)
            }}
          />
          <p>entries</p>
        </div>

        {/* Search */}
        <div className="search">
          <input
            type="text"
            value={query}
            placeholder="Search brands..."
            onChange={(e) => setQuery(e.target.value)}
          />
        </div>
      </section>

      {/* Brand Display section */}
      <section className="display-section">
        {selectedBrand && (
          <BrandDetailsModal
          brand={selectedBrand}
          onClose={closeDetailsModal}
          />
        )}
        
        {<BrandTable
          brands={filteredBrands}
          filteredBrands={filteredBrands}
          loading={loading}
          onEdit={handleEdit}
          onDelete={handleDelete}
          onView={handleViewDetails}
          isSearching={search}
        />}
      </section>

    </main>
  );
}


function BrandPage() {
  return <Layout main={<BrandPageView />} />
}

export default BrandPage;
