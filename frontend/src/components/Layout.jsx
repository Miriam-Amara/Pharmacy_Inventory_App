import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import Header from "./Header";
import Sidebar from "./Sidebar";
import { useAuth } from "../hook/useAuth";
import "./styles/Layout.css"

function Layout({main}){
  const { employee, logout } = useAuth();
  const [displayMenu, setDisplayMenu] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    if (!employee)
    navigate("/login");
  }, [employee]);

    return(
        <div className="container">
            <header className="header">
              <Header
                employee={employee}
                logout={logout}
                displayMenu={displayMenu}
                setDisplayMenu={setDisplayMenu}
              />
            </header>
            
            <div className="main-container">
                {displayMenu &&
                <Sidebar employee={employee} />
                }
                {main}
            </div>
        </div>
    );

}

export default Layout