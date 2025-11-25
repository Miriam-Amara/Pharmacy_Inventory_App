import { useState, useEffect } from "react";

import {
  profileUpdateValidationSchema
} from "../../utils/formInputValidation";
import { fetchMe, updateEmployee } from "../../api/employee";
import Layout from "../../components/Layout";


function useProfileLogic() {
  const [isEditing, setIsEditing] = useState(false);
  const [errors, setErrors] = useState({});
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    first_name: "",
    middle_name: "",
    last_name: "",
    home_address: "",
    role: "",
  });

  useEffect(() => {
    async function loadEmployee() {
      const data = await fetchMe();
      setFormData({...data, middle_name: data.middle_name ?? ""});
    }
    loadEmployee();
  }, []);

  const handleChange = (e) => {
    const {value, name} = e.target;
    setFormData((prev) => ({...prev, [name]: value}));
  };

  const handleIsEditing = (e) => {
    e.preventDefault();
    setIsEditing(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try{
      await profileUpdateValidationSchema.validate(formData, {abortEarly: false});
      await updateEmployee(formData?.id, formData);
    }
    catch (error) {
      console.error("Error in handle submit", error);
      if (error.inner) {
        const newError = {}
        for (const err of error.inner)
          newError[err.path] = err.message
        setErrors(newError);
      }
    }
  };

  return ({
    formData,
    errors,
    isEditing,
    setIsEditing,
    handleChange,
    handleIsEditing,
    handleSubmit
  });
}

function ProfileForm({
  formData, errors, isEditing, setIsEditing, handleChange, handleIsEditing, handleSubmit}) {
  return (
    <form onSubmit={handleSubmit}>

      <div>
        <label>Username:</label>
        <div>
          <input
            type="text"
            name="username"
            value={formData.username}
            disabled={!isEditing}
            readOnly
          />
        </div>
      </div>

      <div>
        <label>Email:</label>
        <div>
          <input
            type="email"
            name="email"
            value={formData.email}
            disabled={!isEditing}
            readOnly
          />
        </div>
      </div>
      
      <div>
        <label>First Name:</label>
        <div>
          <input
            type="text"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
            disabled={!isEditing}
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
            onChange={handleChange}
            disabled={!isEditing}
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
            onChange={handleChange}
            disabled={!isEditing}
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
            onChange={handleChange}
            disabled={!isEditing}
          />
          {errors.home_address && <p>{errors.home_address}</p>}
        </div>
      </div>

      <div>
        <label>Role</label>
        <div>
          <input
            type="text"
            name="role"
            value={formData.role}
            disabled={!isEditing}
            readOnly
          />
        </div>
      </div>

      <div>
        <div>
          <button>Reset Password</button>
        </div>
        <div>
          <button type="button" onClick={handleIsEditing}>Edit</button>
        </div>
        <div>
          <button type="button" onClick={() => setIsEditing(false)}>Cancel</button>
        </div>
        <div>
          <button type="submit">Save</button>
        </div>
      </div>

    </form>
  );
}

function PageView() {
  const {
    formData, errors, isEditing,
    setIsEditing, handleChange, handleIsEditing, handleSubmit} = useProfileLogic();

  return (
    <main>
      <section>

      </section>

      <section>
        <ProfileForm
          formData={formData}
          errors={errors}
          isEditing={isEditing}
          setIsEditing={setIsEditing}
          handleChange={handleChange}
          handleIsEditing={handleIsEditing}
          handleSubmit={handleSubmit}
        />
      </section>
    </main>
  );
}

function ProfilePage() {
  return <Layout main={<PageView />} />
}

export default ProfilePage;
