import { useNavigate } from "react-router-dom";

import api from "../api/api";
import "./styles/Header.css"


function Header({ employee, logout, displayMenu, setDisplayMenu }) {
  
  const username = employee?.username ?? "Guest";
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await api.delete("/auth_session/logout");
      logout();
      navigate("/login");
    } catch (err) {
      console.error("Logout failed:", err);
    }
  };

  return (
    <>
      <div className="header-item">
        <div
          className="menu"
          onClick={() => {setDisplayMenu(!displayMenu);}}
        >
        </div>
        <h5>CIA-PHARMACY</h5>
      </div>

      <div className="header-item">
        <p>{username}</p>
        <button onClick={handleLogout}>
            Logout
        </button>
      </div>  
    </>
  );
}

export default Header;
