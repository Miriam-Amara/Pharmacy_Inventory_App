import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { employeeLoginValidationSchema } from "../../utils/formInputValidation";
import { login } from "../../api/employee";


function useLoginLogic(){
  const [formData, setFormData] = useState({
      email_or_username: "",
      password: "",
    });
    const [errors, setErrors] = useState({});
    const [showPassword, setShowPassword] = useState(false);
    const navigate = useNavigate();
  
    const handleChange = (e) => {
      const {name, value} = e.target;
      setFormData(prev => ({...prev, [name]: value}));
    };
  
    const handleSubmit = async (e) => {
      e.preventDefault();
      try{
        await employeeLoginValidationSchema.validate(formData, {abortEarly: false})
        await login(formData)
  
        setErrors({});
        setFormData({
          email_or_username: "",
          password: "",
        });
        navigate("/profile");
      }
      catch (error) {
        console.error("Error in login handleSubmit", error);
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
      handleChange,
      handleSubmit,
    };
}

function LoginForm({
  formData,
  errors,
  showPassword,
  setShowPassword,
  handleChange,
  handleSubmit,
}) {
  /* Renders login form */

  return (
    <form onSubmit={handleSubmit}>

      <div>
        <label>Email or Username:</label>
        <div>
          <input
            type="text"
            name="email_or_username"
            value={formData.email_or_username}
            placeholder="Enter your email or username"
            onChange={handleChange}
          />
          {errors.email_or_username && <p>{errors.email_or_username}</p>}
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
        <button type="submit">Login</button>
      </div>

    </form>
  );
}

function LoginPage() {
  const {
    formData,
    errors,
    showPassword,
    setShowPassword,
    handleChange,
    handleSubmit
  } = useLoginLogic();

  return (
    <main>
      <section>
        <h3>CIA-PHARMACY</h3>
      </section>
      <section>
        <LoginForm
          formData={formData}
          errors={errors}
          handleChange={handleChange}
          handleSubmit={handleSubmit}
          showPassword={showPassword}
          setShowPassword={setShowPassword}
        />
      </section>
    </main>
  );
}

export default LoginPage;
