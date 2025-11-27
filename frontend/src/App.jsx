import { Routes, Route, Navigate } from "react-router-dom";

import {AuthProvider } from "./pages/auth/AuthProvider.jsx";
import BrandPage from "./pages/admin/BrandPage.jsx";
import CategoryPage from "./pages/admin/CategoryPage.jsx";
import LoginPage from "./pages/auth/login.jsx";
import ProfilePage from "./pages/employees/profile.jsx";
import ProductPage from "./pages/admin/productsPage.jsx";
import RegistrationPage from "./pages/auth/register.jsx";


function App() {
  return(
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegistrationPage />} />
        <Route path="/" element={<RegistrationPage />} />

        <Route path="/brands" element={<BrandPage />} />
        <Route path="/categories" element={<CategoryPage />} />
        <Route path="/products" element={<ProductPage />} />
        <Route path="/profile" element={<ProfilePage />} />
      </Routes>
    </AuthProvider>
  );
}

export default App;
