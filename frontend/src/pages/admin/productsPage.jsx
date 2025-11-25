import { useState } from "react";
import { addDepartment } from "../api/products";



const handleSubmit = (formData) => {
  setFormData((prev) => {...prev, formData});

  const response = async () => {
    await addDepartment();
  }
}

const handleChange = (formData) => {
  setFormData((prev) => {...prev, formData});
}

function FormInput() {
  const { formData, setFormData } = useState({});
  setFormData({product_name: ""});

  return formData
}

function ProductsPage() {
  return (
    <div>
      <button>Register</button>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Name</label>
          <input type="text" name="product_name" value="" onChange={handleChange} />
        </div>
        <button>Submit</button>
      </form>
    </div>
  );
}

export default ProductsPage