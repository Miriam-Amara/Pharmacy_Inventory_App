import "./sidebar.css"


function Sidebar(){
    return(
        <aside className="sidebar-nav">
                <ul className="main-nav">
                    {/* <li></li> */}
                    <li><a href="/dashboard">Dashboard</a></li>
                </ul>

                <ul className="main-nav">
                    {/* <li><img src="content_icon" alt="Content" className="nav-icon" /></li> */}
                    <li>
                        Inventory
                        <ul className="inner-nav">
                            <li><a href="/brands">Brands</a></li>
                            <li><a href="/categories">Categories</a></li>
                            <li><a href="/products">Products</a></li>
                    </ul>
                    </li>
                </ul>
            
                <ul className="main-nav">
                    {/* <li><img src="support_icon" alt="Support" className="nav-icon" /></li> */}
                    <li>
                        Transactions
                        <ul className="inner-nav">
                            <li><a href="/sales">Sales</a></li>
                            <li><a href="/purchase_orders">Purchase Order</a></li>
                            <li><a href="/purchase_order_items">Purchase Order Item</a></li>
                    </ul>
                    </li>
                </ul>

                <ul className="main-nav">
                    {/* <li></li> */}
                    <li>
                        Users
                        <ul className="inner-nav">
                            <li><a href="/employees">Manage Users</a></li>
                    </ul>
                    </li>
                </ul>

                <ul className="main-nav">
                    {/* <li><img src="profile_icon" alt="Profile" className="nav-icon" /></li> */}
                    <li><a href="/profile">Profile</a></li>
                </ul>
        </aside>
    );
}

export default Sidebar