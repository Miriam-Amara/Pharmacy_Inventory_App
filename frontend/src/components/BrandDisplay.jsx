/* */

import deleteIcon from '../assets/delete_icon.png';
import editIcon from "../assets/edit_icon.png";
import viewIcon1 from "../assets/view_icon1.png";

export function BrandDetailsModal({brand, onClose}) {
  if (!brand)
    return null;

  return (
    <div className="details-modal-container">
      <div className="details-modal">
        <button onClick={onClose}>Close</button>

        <h5>Brand Details</h5>
        
        <div className="details">
          <div className="details-title">
            <p><span>ID:</span> {brand.id}</p>
            <p><span>Date Created:</span> {new Date(brand.created_at).toLocaleString()}</p>
            <p><span>Last Updated:</span> {new Date(brand.created_at).toLocaleString()}</p>
            <p><span>Added By:</span> {brand.added_by}</p>
          </div>

          <div className="details-content">
            <p><span>Brand Name:</span> {brand.name}</p>
            <p><span>Active:</span> {brand.is_active ? "Yes" : "No"}</p>
          </div>
        </div>

      </div>
    </div>
  );
}


export function BrandTable({brands, loading, onDelete, onEdit, onView, isSearching}) {
  if (loading)
    return <p>Loading brands...</p>
  if (isSearching && brands.length === 0)
    return <p>No match found.</p>;
  if (!isSearching && brands.length === 0)
    return <p>No brands found. Please add some brands.</p>;
  
  return (
      <table className="content-table">
        <thead>
          <tr>
            <th>Brand Name</th>
            <th>Is Active</th>
            <th>Date Added</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {brands.map((brand) => (
            <tr key={brand.id}>
              <td>{brand.name}</td>
              <td>{brand.is_active ? "Yes" : "No"}</td>
              <td>{new Date(brand.created_at).toLocaleDateString()}</td>
              <td className='table-actions'>
                <button
                  onClick={() => onView(brand)}
                  className="btn btn-info-icon"
                >
                  <img src={viewIcon1} alt="Info" />
                </button>

                <button
                  onClick={() => onEdit(brand)}
                  className="btn btn-edit-icon"
                >
                  <img src={editIcon} alt="Edit" />
                </button>

                <button
                  onClick={() => onDelete(brand)}
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
