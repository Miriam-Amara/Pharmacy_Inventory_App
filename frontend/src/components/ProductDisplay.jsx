/* */

import deleteIcon from '../assets/delete_icon.png';
import editIcon from "../assets/edit_icon.png";
import viewIcon1 from "../assets/view_icon1.png";


export function DisplayProductFormModal({
  formData, errors, mode, brands, categories,
  handleFetchBrands, handleFetchCategories,
  handleChange, handleSubmit, resetForm, setShowForm
}) {
  
  return (
    <div className="modal-container">
      <div className="modal">
        <button
          onClick={() => {resetForm(); setShowForm(false);}}
        >
          Cancel
        </button>

        <div>
          {mode == "add" ? "Add" : "Edit"} Product
        </div>

        <form onSubmit={handleSubmit} className="form">
          <div className="form-item">
            <label>Barcode:</label>
            <div>
              <input
                type="text"
                name="barcode"
                value={formData.barcode}
                onChange={handleChange}
              />
              {errors.barcode && <p>{errors.barcode}</p>}
            </div>
          </div>

          <div className="form-item">
            <label>Product Name:</label>
            <div>
              <input
                type="text"
                name="name"
                value={formData.name}
                placeholder="Enter product name"
                onChange={handleChange}
              />
              {errors.name && <p>{errors.name}</p>}
            </div>
          </div>

          <div className="form-item">
            <label>Unit Cost Price (₦):</label>
            <div>
              <input
                type="text"
                name="unit_cost_price"
                value={formData.unit_cost_price}
                placeholder="Enter unit cost price"
                onChange={handleChange}
              />
              {errors.unit_cost_price && <p>{errors.unit_cost_price}</p>}
            </div>
          </div>

          <div className="form-item">
            <label>Unit Selling Price (₦):</label>
            <div>
              <input
                type="text"
                name="unit_selling_price"
                value={formData.unit_selling_price}
                placeholder="Enter unit selling price"
                onChange={handleChange}
              />
              {errors.unit_selling_price && <p>{errors.unit_selling_price}</p>}
            </div>
          </div>

          <div className="form-item">
            <label>Brand:</label>
            <div>
              <select
                name="brand_id"
                value={formData.brand_id}
                onClick={() => {handleFetchBrands();}}
                onChange={handleChange}
              >
                <option value="" disabled hidden>Select brand</option>
                {brands.map((b) => (
                  <option key={b.id} value={b.id}>
                    {b.name}
                  </option>
                ))}
                <option value="other">other:</option>
              </select>
              {errors.brand_id && <p>{errors.brand_id}</p>}
            </div>

            {formData.brand_id === "other" && (
            <div>
              <input
                type="text"
                name="brand_name"
                placeholder="Enter brand name"
                value={formData.brand_name || ""}
                onChange={handleChange}
                required
              />
              {errors.brand_name && <p>{errors.brand_name}</p>}
            </div>
          )}
          </div>
          
          <div className="form-item">
            <label>Category:</label>
            <div>
              <select
                name="category_id"
                value={formData.category_id}
                onClick={() => {handleFetchCategories();}}
                onChange={handleChange}
              >
                <option value="" disabled hidden>Select category</option>
                {categories.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name}
                  </option>
                ))}
              </select>
              {errors.category_id && <p>{errors.category_id}</p>}
            </div>
          </div>

          <div className="form-item">
            <label>Created At:</label>
            <div>
              <input
              type="datetime-local"
              name="created_at"
              value={formData.created_at}
              onChange={handleChange}
            />
            </div>
          </div>

          <div className="form-item">
            <label>Last Updated:</label>
            <div>
              <input
              type="datetime-local"
              name="last_updated"
              value={formData.last_updated}
              onChange={handleChange}
            />
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


export function DisplayProductsTable({
  products, handleViewDetails, handleEdit, handleDelete
}) {
  return (
    <table className="content-table">
      <thead>
        <tr>
          <th>Product Name</th>
          <th>Category</th>
          <th>Brand</th>
          <th>Quantity</th>
          <th>Cost Price</th>
          <th>Selling Price</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {products.map((product) => (
          <tr key={product.id}>
            <td>{product.name}</td>
            <td>{product.category_name}</td>
            <td>{product.brand_name}</td>
            <td>{product.quantity_in_stock}</td>
            <td>{product.unit_cost_price}</td>
            <td>{product.unit_selling_price}</td>
            <td className='table-actions'>
              <button
                type="button"
                onClick={() => handleViewDetails(product)}
                className="btn btn-info-icon"
              >
                <img src={viewIcon1} alt="Info" />
              </button>

              <button
                type="button"
                onClick={() => handleEdit(product)}
                className="btn btn-edit-icon"
              >
                <img src={editIcon} alt="Edit" />
              </button>

              <button
                type="button"
                onClick={() => handleDelete(product)}
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


export function DisplayProductsReorderingPoint({products}) {
  return (
    <table className="content-table">
      <thead>
        <tr>
          <th>Product Name</th>
          <th>Quantity In Stock</th>
          <th>Reorder</th>
          <th>Reorder Quantity</th>
        </tr>
      </thead>
      <tbody>
        {products.map((product) => (
          <tr key={product.id}>
            <td>{product.name}</td>
            <td>{product.quantity_in_stock}</td>
            <td>{product.is_below_reorder}</td>
            <td>{product.economic_ordering_quantity}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}


export function DisplayProductsGrid() {

}


export function DisplayProductDetailsModal({product, setSelectedProduct}) {
  return(
    <div className="details-modal-container">
      <div className="details-modal">
        <button
          type="button"
          onClick={() => {setSelectedProduct(null)}}
        >
          Close
        </button>

        <h5>Product Details</h5>

        <div className="details">
          <div className="details-title">
            <p><span>ID:</span> {product.id}</p>
            <p><span>Date Created:</span> {new Date(product.created_at).toLocaleString()}</p>
            <p><span>Last Updated:</span> {new Date(product.last_updated).toLocaleString()}</p>
            <p><span>Added By:</span> {product.added_by}</p>
          </div>
          <div className="details-content">
            <p><span>Product Name:</span> {product.name}</p>
            <p><span>Category:</span> {product.category_name}</p>
            <p><span>Brand:</span> {product.brand_name}</p>
            <p><span>Quantity In Stock:</span> {product.quantity_in_stock}</p>
            <p><span>ReorderPoint:</span> {product.is_below_reorder}</p>
            <p><span>Reorder Quantity:</span> {product.economic_ordering_quantity}</p>
            <p><span>Unit Cost Price:</span> ₦ {product.unit_cost_price}</p>
            <p><span>Unit Selling Price:</span> ₦ {product.unit_selling_price}</p>
          </div>
        </div>
      </div>
    </div>
  );
}