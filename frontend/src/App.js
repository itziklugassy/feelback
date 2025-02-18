import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.rtl.min.css';
import HomePage from './pages/HomePage';
import ProjectPage from './pages/ProjectPage';
import LoginPage from './pages/LoginPage';
import NavigationBar from './components/Navbar';

function App() {
    return (
        <Router>
            <div dir="rtl">
                <NavigationBar />
                <Routes>
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/" element={<HomePage />} />
                    <Route path="/project/:id" element={<ProjectPage />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;