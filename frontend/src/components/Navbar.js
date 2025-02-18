import React from 'react';
import { Navbar, Container, Nav } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import { isAuthenticated, logout, getUsername } from '../services/api';

const NavigationBar = () => {
  const navigate = useNavigate();
  const authenticated = isAuthenticated();
  const username = getUsername();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <Navbar bg="dark" variant="dark" expand="lg" dir="rtl">
      <Container>
        <Navbar.Brand as={Link} to="/">מערכת דירוגים</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link as={Link} to="/">דף הבית</Nav.Link>
          </Nav>
          <Nav>
            {authenticated ? (
              <>
                <Nav.Link>{username} שלום</Nav.Link>
                <Nav.Link onClick={handleLogout}>התנתק</Nav.Link>
              </>
            ) : (
              <Nav.Link as={Link} to="/login">התחבר</Nav.Link>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default NavigationBar;