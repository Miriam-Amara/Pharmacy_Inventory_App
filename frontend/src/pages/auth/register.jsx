import { useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  employeeRegistrationValidationSchema
} from "../../utils/formInputValidation";
import { registerApi } from "../../api/employee";


function useRegistrationLogic() {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirm_password: "",
    first_name: "",
    middle_name: "",
    last_name: "",
    home_address: "",
    role: "salesperson",
    is_admin: false
  });
  const [errors, setErrors] = useState({});
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const {name, value} = e.target;
    setFormData(prev => ({...prev, [name]: value}));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try{
      await employeeRegistrationValidationSchema.validate(formData, {abortEarly: false})

      const data = {
        ...formData,
        middle_name: formData.middle_name.trim() === "" ? null : formData.middle_name
      }
      await registerApi(data)

      setErrors({});
      setFormData({
        username: "",
        email: "",
        password: "",
        confirm_password: "",
        first_name: "",
        middle_name: "",
        last_name: "",
        home_address: "",
        role: "salesperson",
        is_admin: false
      });
      navigate("/login");
    }
    catch (error) {
      if (error.inner) {
        const newError = {}
        for (let err of error.inner)
          newError[err.path] = err.message;
        setErrors(newError);
      }
    }
  };

  return {
    formData,
    errors,
    showPassword,
    setShowPassword,
    showConfirmPassword,
    setShowConfirmPassword,
    handleChange,
    handleSubmit,
  };
}

function RegistrationForm({
  formData,
  errors,
  showPassword,
  setShowPassword,
  showConfirmPassword,
  setShowConfirmPassword,
  handleChange,
  handleSubmit,
}) {
  /* Renders registration form */

  return (
    <form onSubmit={handleSubmit}>

      <div>
        <label>Username:</label>
        <div>
          <input
            type="text"
            name="username"
            value={formData.username}
            placeholder="Enter your username"
            onChange={handleChange}
          />
          {errors.username && <p>{errors.username}</p>}
        </div>
      </div>

      <div>
        <label>Email:</label>
        <div>
          <input
            type="email"
            name="email"
            value={formData.email}
            placeholder="Enter your email"
            onChange={handleChange}
          />
          {errors.email && <p>{errors.email}</p>}
        </div>
      </div>

      <div>
        <label>Password:</label>
        <div>
          <div>
            <input
            type= {showPassword ? "text" : "password"}
            name="password"
            value={formData.password}
            placeholder="Enter your password"
            onChange={handleChange}
          />
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
          >
            {showPassword ? "👁️" : "🙈"}
          </button>
          </div>
          {errors.password && <p>{errors.password}</p>}
        </div>
      </div>

      <div>
        <label>Confirm Password:</label>
        <div>
          <div>
            <input
            type={showConfirmPassword ? "text" : "password"}
            name="confirm_password"
            value={formData.confirm_password}
            placeholder="Confirm your password"
            onChange={handleChange}
          />
          <button
            type="button"
            onClick={() => setShowConfirmPassword(!showConfirmPassword)}
          >
            {showConfirmPassword ? "👁️" : "🙈"}
          </button>
          </div>
          {errors.confirm_password && <p>{errors.confirm_password}</p>}
        </div>
      </div>
      
      <div>
        <label>First Name:</label>
        <div>
          <input
            type="text"
            name="first_name"
            value={formData.first_name}
            placeholder="Enter your first name"
            onChange={handleChange}
          />
          {errors.first_name && <p>{errors.first_name}</p>}
        </div>
      </div>

      <div>
        <label>Middle Name:</label>
        <div>
          <input
            type="text"
            name="middle_name"
            value={formData.middle_name}
            placeholder="Enter your middle name"
            onChange={handleChange}
          />
          {errors.middle_name && <p>{errors.middle_name}</p>}
        </div>
      </div>

      <div>
        <label>Last Name:</label>
        <div>
          <input
            type="text"
            name="last_name"
            value={formData.last_name}
            placeholder="Enter your last name"
            onChange={handleChange}
          />
          {errors.last_name && <p>{errors.last_name}</p>}
        </div>
      </div>

      <div>
        <label>Home Address:</label>
        <div>
          <input
            type="text"
            name="home_address"
            value={formData.home_address}
            placeholder="Enter your home address"
            onChange={handleChange}
          />
          {errors.home_address && <p>{errors.home_address}</p>}
        </div>
      </div>

      <div>
        <button type="submit">Register</button>
      </div>

    </form>
  );
}


function RegistrationPage() {
  let {
    formData,
    errors,
    showPassword,
    setShowPassword,
    showConfirmPassword,
    setShowConfirmPassword,
    handleChange,
    handleSubmit
  } = useRegistrationLogic();

  return (
    <main>
      <section>
        <h3>CIA-PHARMACY</h3>
      </section>
      <section>
        <RegistrationForm
          formData={formData}
          errors={errors}
          handleChange={handleChange}
          handleSubmit={handleSubmit}
          showPassword={showPassword}
          setShowPassword={setShowPassword}
          showConfirmPassword={showConfirmPassword}
          setShowConfirmPassword={setShowConfirmPassword}
        />
      </section>
    </main>
  );
}

export default RegistrationPage;
