/* */

import useBrandLogic from "../../hook/BrandLogic";
import BrandForm from "../../components/BrandForm";
import { BrandTable, BrandDetailsModal } from "../../components/BrandDisplay";
import Layout from "../../components/Layout";


function BrandPageView() {
  const {
    errors,
    filteredBrands,
    formData,
    formMode,
    loading,
    pageSizeInput,
    pageNumInput,
    query,
    selectedBrand,
    search,
    showForm,
    setFormMode,
    setPageSize,
    setPageNum,
    setPageSizeInput,
    setPageNumInput,
    setShowForm,
    setQuery,
    closeDetailsModal,
    handleChange,
    handleDelete,
    handleEdit,
    handleSubmit,
    handleViewDetails,
    resetForm,
  } = useBrandLogic();

  return (
    <main>

      {/* Info section */}
      <section>
        <h2>Brands</h2>
        <p>View, add, edit and delete brands.</p>
      </section>

      {/* Control Section - forms, search, pagination */}
      <section>

        {/* Form */}
        <div>
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
        <div>
          <div>
            <label>Page Size:</label>
            <input
              type="number"
              name="pageSize"
              value={pageSizeInput}
              min={1}
              onChange={(e) => {
                const val = Number(e.target.value)
                setPageSizeInput(val < 1 ? 1 : val)
              }}
            />
          </div>

          <div>
            <label>Next Page:</label>
            <input
              type="number"
              name="pageNum"
              value={pageNumInput}
              min={1}
              onChange={(e) => {
                const val = Number(e.target.value)
                setPageNumInput(val < 1 ? 1 : val)
              }}
            />
          </div>

          <button
            onClick={() => {
              setPageSize(pageSizeInput);
              setPageNum(pageNumInput);
            }}
          >
            Enter
          </button>
        </div>

        {/* Search */}
        <div>
          <input
            type="text"
            value={query}
            placeholder="Search brands..."
            onChange={(e) => setQuery(e.target.value)}
          />
        </div>
      </section>

      {/* Brand Display section */}
      <section>
        {<BrandTable
          brands={filteredBrands}
          filteredBrands={filteredBrands}
          loading={loading}
          onEdit={handleEdit}
          onDelete={handleDelete}
          onView={handleViewDetails}
          isSearching={search}
        />}

        {selectedBrand && (
          <BrandDetailsModal
          brand={selectedBrand}
          onClose={closeDetailsModal}
          />
        )}
      </section>

    </main>
  );
}


function BrandPage() {
  return <Layout main={<BrandPageView />} />
}

export default BrandPage;
