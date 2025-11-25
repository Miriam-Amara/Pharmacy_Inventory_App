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
    <>
      <div>
        <button onClick={resetForm}>Cancel</button>

        <form onSubmit={handleSubmit}>
          <div>
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

          <div>
            <label>Is brand still active?</label>
            <select name="is_active" value={String(formData.is_active)} onChange={handleChange}>
              <option value="true">Yes</option>
              <option value="false">No</option>
            </select>
          </div>

          <div>
            <button type="submit">{formMode === "edit" ? "Update" : "Add"}</button>
          </div>
        </form>        
      </div> 
    </>
  );
}

export default BrandForm;