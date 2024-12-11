
import { AlertLink, Container } from 'react-bootstrap';
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/Home.js';
import Album from './pages/Album.js';
import NavBar from './components/Navbar/NavBar.js';

function App() {
  return (
    <Router>
      <NavBar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/albums/:id" element={<Album />} />
      </Routes>
    </Router>
  );
}

export default App;
