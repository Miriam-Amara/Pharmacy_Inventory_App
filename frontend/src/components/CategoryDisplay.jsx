/* */

import deleteIcon from '../assets/delete_icon.png';
import editIcon from "../assets/edit_icon.png";
import viewIcon1 from "../assets/view_icon1.png";

export function DisplayCategoryFormModal(props) {
  const {
    formData, errors, mode,
    handleChange, handleSubmit, resetForm

  } = props;

  return (
    <div className="modal-container">
      <div className="modal">
        <button onClick={() => {resetForm();}}>Cancel</button>

        <div>
          {mode == "add" ? "Add" : "Edit"} Category
        </div>

        <form onSubmit={handleSubmit} className="form">
          <div className="form-item">
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

          <div className="form-item">
            <label>Description:</label>
            <div>
              <textarea
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
    </div>
  );
}


export function DisplayCategoriesTable(props) {
  const {categories, handleViewDetails, handleEdit, handleDelete} = props
  return (
    <table className="content-table">
      <thead>
        <tr>
          <th>Category Name</th>
          <th>Date Created</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {categories.map((category) => (
          <tr key={category.id}>
            <td>{category.name}</td>
            <td>{new Date(category.created_at).toLocaleDateString()}</td>
            <td className='table-actions'>
              <button
                type="button"
                onClick={() => handleViewDetails(category)}
                className="btn btn-info-icon"
              >
                <img src={viewIcon1} alt="Info" />
              </button>

              <button
                type="button"
                onClick={() => handleEdit(category)}
                className="btn btn-edit-icon"
              >
                <img src={editIcon} alt="Edit" />
              </button>

              <button
                type="button"
                onClick={() => handleDelete(category)}
                className="btn btn-danger-icon"
              >
                <img src={deleteIcon} alt="Delete" />
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
    <div className="details-modal-container">
      <div className="details-modal">
        <button
          type="button"
          onClick={() => {setSelectedCategory(null)}}
        >
          Close
        </button>

        <h5>Category Details</h5>

        <div className="details">
          <div className="details-title">
            <p><span>ID:</span> {category.id}</p>
            <p><span>Date Created:</span> {new Date(category.created_at).toLocaleString()}</p>
            <p><span>Last Updated:</span> {new Date(category.last_updated).toLocaleString()}</p>
            <p><span>Added By:</span> {category.added_by}</p>
          </div>

          <div className="details-content">
            <p><span>Category Name:</span> {category.name}</p>
            <p><span>Description:</span> {category.description}</p>
          </div>
        </div>
      </div>
    </div>
  );
}