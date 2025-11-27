import React, { createContext, useState } from "react";

import { fetchMe } from "../../api/employee.js";

// eslint-disable-next-line react-refresh/only-export-components
export const AuthContext = createContext();

export  function AuthProvider({ children }) {
  const [employee, setEmployee] = useState(null);
  const [loading, setLoading] = useState(true);

  async function loadUser() {
      try {
        const data = await fetchMe();
        setEmployee(data);
        return data;
      } catch {
        setEmployee(null);
      } finally {
        setLoading(false);
      }
    }

  const login = async () => {
    const data = await loadUser();
    setEmployee(data);
  };

  const logout = () => {
    setEmployee(null);
  };

  return (
    <AuthContext.Provider value={{ employee, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
