/* */


export function DisplayCategoryFormModal(props) {
  const {
    formData, errors, mode,
    handleChange, handleSubmit, resetForm

  } = props;

  return (
    <div>

      <button onClick={() => {resetForm();}}>Cancel</button>

      <div>
        {mode == "add" ? "Add" : "Edit"} category
      </div>

      <form onSubmit={handleSubmit}>
        <div>
          <label>Category Name:</label>
          <div>
            <input
              type="text"
              name="name"
              value={formData.name}
              placeholder="Enter category name"
              onChange={handleChange}
            />
            {errors.name && <p>{errors.name}</p>}
          </div>
        </div>

        <div>
          <label>Description:</label>
          <div>
            <input
              type="text"
              name="description"
              value={formData.description}
              placeholder="Enter category description"
              onChange={handleChange}
            />
            {errors.description && <p>{errors.description}</p>}
          </div>
        </div>

        <button type="submit">
          {mode == "add" ? "Save" : "Update"}
        </button>
      </form>
    </div>
  );
}


export function DisplayCategoriesTable(props) {
  const {categories, handleViewDetails, handleEdit, handleDelete} = props
  return (
    <table>
      <thead>
        <tr>
          <th>Category Name</th>
          <th>Description</th>
          <th>Date Created</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {categories.map((category) => (
          <tr key={category.id}>
            <td>{category.name}</td>
            <td>{category.description}</td>
            <td>{new Date(category.created_at).toLocaleDateString()}</td>
            <td>
              <button
                type="button"
                onClick={() => handleViewDetails(category)}
              >
                Details
              </button>

              <button
                type="button"
                onClick={() => handleEdit(category)}
              >
                Edit
              </button>

              <button
                type="button"
                onClick={() => handleDelete(category)}
              >
                Delete
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}


export function DisplayCategoryDetailsModal({category, setSelectedCategory}) {
  return(
    <div>
      <button
        type="button"
        onClick={() => {setSelectedCategory(null)}}
      >
        Close
      </button>
      <h4>Category Details</h4>
      <p>ID: {category.id}</p>
      <p>Date Created: {new Date(category.created_at).toLocaleString()}</p>
      <p>Last Updated: {new Date(category.last_updated).toLocaleString()}</p>
      <p>Added By: {category.added_by}</p>
      <p>Category Name: {category.name}</p>
      <p>Description: {category.description}</p>
    </div>
  );
}