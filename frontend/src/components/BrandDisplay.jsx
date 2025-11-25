/* */


export function BrandDetailsModal({brand, onClose}) {
  if (!brand)
    return null;

  return (
    <div>
      <h3>Brand Details</h3>
      
      <div>
        <p>ID: {brand.id}</p>
        <p>Name: {brand.name}</p>
        <p>Active: {brand.is_active ? "Yes" : "No"}</p>
        <p>Date Created: {brand.created_at}</p>
        <p>Last Updated: {brand.last_updated}</p>
        <p>Added By: {brand.added_by}</p>
      </div>

      <div>
        <button onClick={onClose}>Close</button>
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
      <table>
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
              <td>
                <button onClick={() => onView(brand)}>View</button>
                <button onClick={() => onEdit(brand)}>Edit</button>
                <button onClick={() => onDelete(brand)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
  );
}
