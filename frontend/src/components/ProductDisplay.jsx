/* */

import ProductPage from "../pages/admin/productsPage";


export function DisplayProductFormModal({
  formData, errors, mode, brands, categories,
  handleFetchBrands, handleFetchCategories,
  handleChange, handleSubmit, resetForm, setShowForm
}) {
  
  return (
    <div>

      <button
        onClick={() => {resetForm(); setShowForm(false);}}
      >
        Cancel
      </button>

      <div>
        {mode == "add" ? "Add" : "Edit"} Product
      </div>

      <form onSubmit={handleSubmit}>
        <div>
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

        <div>
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

        <div>
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

        <div>
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

        <div>
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
        
        <div>
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

        <div>
          <label>Created At:</label>
          <input
            type="datetime-local"
            name="created_at"
            value={formData.created_at}
            onChange={handleChange}
          />
        </div>

        <div>
          <label>Last Updated:</label>
          <input
            type="datetime-local"
            name="last_updated"
            value={formData.last_updated}
            onChange={handleChange}
          />
        </div>

        <button type="submit">
          {mode == "add" ? "Save" : "Update"}
        </button>
      </form>
    </div>
  );
}


export function DisplayProductsTable({
  products, handleViewDetails, handleEdit, handleDelete
}) {
  return (
    <table>
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
            <td>
              <button
                type="button"
                onClick={() => handleViewDetails(product)}
              >
                Details
              </button>

              <button
                type="button"
                onClick={() => handleEdit(product)}
              >
                Edit
              </button>

              <button
                type="button"
                onClick={() => handleDelete(product)}
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


export function DisplayProductsReorderingPoint({products}) {
  return (
    <table>
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
    <div>
      <button
        type="button"
        onClick={() => {setSelectedProduct(null)}}
      >
        Close
      </button>
      <h4>Product Details</h4>
      <p>ID: {product.id}</p>
      <p>Date Created: {new Date(product.created_at).toLocaleString()}</p>
      <p>Last Updated: {new Date(product.last_updated).toLocaleString()}</p>
      <p>Added By: {product.added_by}</p>
      <p>Product Name: {product.name}</p>
      <p>Category: {product.category_name}</p>
      <p>Brand: {product.brand_name}</p>
      <p>Quantity In Stock: {product.quantity_in_stock}</p>
      <p>Reorder: {product.is_below_reorder}</p>
      <p>Reorder Quantity: {product.economic_ordering_quantity}</p>
      <p>Unit Cost Price: {product.unit_cost_price}</p>
      <p>Unit Selling Price: {product.unit_selling_price}</p>
    </div>
  );
}