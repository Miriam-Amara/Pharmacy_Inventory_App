/* */

function BrandForm({
  formData,
  errors,
  formMode,
  handleChange,
  handleSubmit,
  resetForm,
}) {

  return (
    <div className="modal-container">
      <div className="modal">
        <button onClick={resetForm}>Cancel</button>

        <div>
          {formMode == "add" ? "Add" : "Edit"} Brand
        </div>

        <form onSubmit={handleSubmit} className="form">
          <div className="form-item">
            <label>Brand Name:</label>
            <div>
              <input
                type="text"
                name="name"
                value={formData.name}
                placeholder="Enter brand name"
                onChange={handleChange}
              />
              {errors.name && <p>{errors.name}</p>}
            </div>
          </div>

          <div className="form-item">
            <label>Is brand still active?</label>
            <select name="is_active" value={String(formData.is_active)} onChange={handleChange}>
              <option value="true">Yes</option>
              <option value="false">No</option>
            </select>
          </div>

          <button type="submit">{formMode === "edit" ? "Update" : "Add"}</button>
        </form>        
      </div> 
    </div>
  );
}

export default BrandForm;