import { useState } from "react";
import { Link } from "react-router-dom";

import "./styles/sidebar.css"



export default function Sidebar({employee}){
  const [displayInventory, setDisplayInventory] = useState(false);
  const [displayTransactions, setDisplayTransactions] = useState(false);

  const admin = employee?.is_admin ?? false;
  
  return(
      <aside className="sidebar-nav">
        {admin && <div className="dashboard"><Link to="/dashboard">Dashboard</Link></div>}
        {admin &&
        <ul>
            <li className="inventory" onClick={() => {setDisplayInventory(!displayInventory)}}>
                Inventory
                {displayInventory &&
                <ul className="sidebar-inner-nav">
                  <li className="brand"><Link to="/brands">Brands</Link></li>
                  <li className="category"><Link to="/categories">Categories</Link></li>
                  <li className="product"><Link to="/products">Products</Link></li>
                </ul>}
            </li>
        </ul>
        }
        {admin &&
        <ul>
          <li className="transaction" onClick={() => {setDisplayTransactions(!displayTransactions)}}>
            Transactions
            {displayTransactions &&
            <ul className="sidebar-inner-nav">
              <li className="sale_order"><Link to="/sales_orders">Sales Orders</Link></li>
              <li className="sale"><Link to="/sales">Sales</Link></li>
              <li className="purchase_order"><Link to="/purchase_orders">Purchase Orders</Link></li>
              <li className="purchase"><Link to="/purchases">Purchases</Link></li>
            </ul>
            }
          </li>
        </ul>
        }
        {!admin && <div className="sale_order"><Link to="/sales_orders">Sales Orders</Link></div>}
        {admin && <div className="employee"><Link to="/employees">Employees</Link></div>}
        <div className="profile"><Link to="/profile">Profile</Link></div>
      </aside>
  );
}
