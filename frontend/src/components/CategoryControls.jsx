/* */


// returns a button which onClick displays form to add category
export const AddCategory = ({setMode, setShowForm}) => (
    <button
      type="button"
      onClick={() => {setMode("add"); setShowForm(true);}}
    >
      Add Category
    </button>
  );

// sets page size
export const Pagination = ({pageSize, setPageSize}) => (
  <>
    <p>Show</p>
    <input
      type="number"
      name="pageSize"
      value={pageSize}
      min={1}
      onChange={(e) => {
        const value = e.target.value
        setPageSize(Number(value));
      }}
    />
    <p>entries</p>
  </>
);

export const SearchCategory = ({search, setSearch}) => {
  return (
    <>
      <input
        type="text"
        name="search"
        value={search}
        placeholder="Search categories..."
        onChange={(e) => {setSearch(e.target.value)}}
      />
    </>
  );
}
