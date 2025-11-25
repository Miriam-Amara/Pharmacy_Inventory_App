/* */


// returns a button which onClick displays form to add category
export const AddCategory = ({setMode, SetShowForm}) => (
    <button
      type="button"
      onClick={() => {setMode("add"), SetShowForm(true);}}
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
      <p>Search</p>
      <input
        type="text"
        name="search"
        value={search}
        onChange={(e) => {
          const value = e.target.value
          if (value.length <= 8 && value.length % 2 === 0) {
          setSearch(value)}
        }}
      />
    </>
  );
}
