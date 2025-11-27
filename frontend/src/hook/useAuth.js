import { useContext } from "react";
import { AuthContext } from "../pages/auth/AuthProvider.jsx"

export function useAuth() {
  return useContext(AuthContext);
}
