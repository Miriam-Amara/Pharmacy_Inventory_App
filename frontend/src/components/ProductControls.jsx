/* */


export const AddProduct = ({setMode, setShowForm}) => (
  <button
    type="button"
    onClick={() => {setMode("add"); setShowForm(true);}}
  >
    AddProduct
  </button>
);

export const FilterProductByCategory = ({
  category, categories, handleFetchCategories, handleFetchFilteredProducts
}) => (
  <>
    <select
      name="category_id"
      value={category.category_id}
      onClick={() => {handleFetchCategories();}}
      onChange={(e) => {handleFetchFilteredProducts(e, "category");}}
    >
      <option value="" disabled hidden>Select category</option>
      {categories.map((c) => (
        <option key={c.id} value={c.id}>
          {c.name}
        </option>
      ))}
    </select>
  </>
);

export const FilterProductByBrand = ({
  brand, brands, handleFetchBrands, handleFetchFilteredProducts
}) => (
  <>
    <select
      name="brand_id"
      value={brand.brand_id}
      onClick={() => {handleFetchBrands();}}
      onChange={(e) => {handleFetchFilteredProducts(e, "brand");}}
    >
      <option value="" disabled hidden>Select brand</option>
      {brands.map((b) => (
        <option key={b.id} value={b.id}>
          {b.name}
        </option>
      ))}
    </select>
  </>
);

export const SearchProduct = (search, setSearch) => (
  <>
    <p>Search</p>
    <input
      type="text"
      name="search"
      value={search}
      placeholder="Search product"
      onChange={(e) => {setSearch(e.target.value)}}
    />
  </>
);

export const Pagination = (pageSize, setPageSize) => (
  <>
    <p>Show</p>
    <input
      type="text"
      name="pageSize"
      value={pageSize}
      onChange={(e) => {setPageSize(Number(e.target.value))}}
    />
    <p>entries</p>
  </>
);
