import React from "react";
import { Navbar } from "react-bootstrap";
import { Link } from "react-router-dom";
import './NavBar.css';

const NavBar = () => {
    return (
        <nav className="navbar">
            <div className="breadcrumb">
                <Link to="/" className="breadcrumb-item">MyMusicMaestro</Link>
                <span className="breadcrumb-item"></span>
            </div>
        </nav>
    );
}

export default NavBar;