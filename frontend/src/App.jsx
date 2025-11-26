import { Routes, Route } from "react-router-dom";

import BrandPage from "./pages/admin/BrandPage.jsx";
import CategoryPage from "./pages/admin/CategoryPage.jsx";
import LoginPage from "./pages/auth/login.jsx";
import ProfilePage from "./pages/employees/profile.jsx";
import ProductPage from "./pages/admin/productsPage.jsx";
import RegistrationPage from "./pages/auth/register.jsx";


function App() {
  return(
    <Routes>
      <Route path="/brands" element={<BrandPage />} />
      <Route path="/categories" element={<CategoryPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/profile" element={<ProfilePage />} />
      <Route path="/products" element={<ProductPage />} />
      <Route path="/register" element={<RegistrationPage />} />
      <Route path="/" element={<RegistrationPage />} />
    </Routes>
  );
}

export default App;
