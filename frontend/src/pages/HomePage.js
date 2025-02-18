import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { getProjects } from '../services/api';
import './HomePage.css';

const HomePage = () => {
  const [projects, setProjects] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const data = await getProjects();
        setProjects(data);
      } catch (error) {
        console.error('Error fetching projects:', error);
      }
    };
    fetchProjects();
  }, []);

  return (
    <div className="home-page">
      <div className="hero-section">
        <Container>
          <div className="logo-ruvni">
            <img 
              src="ruvnismalllogo.png" 
              alt="Ruvni Logo" 
            />
          </div>
          <div className="logo-container">
            <img 
              src="/feebackicon.png" 
              alt="Feedback Logo" 
            />
          </div>
          <h1 className="hero-title">הפרויקטים שלנו</h1>
        </Container>
      </div>
      
      <Container dir="rtl" className="projects-container">
        <Row xs={1} md={2} lg={3} className="g-4">
          {projects.map((project) => (
            <Col key={project.id}>
              <Card 
                onClick={() => navigate(`/project/${project.id}`)}
                className="project-card"
              >
                {project.thumbnail && (
                  <div className="card-image-wrapper">
                    <Card.Img 
                      variant="top" 
                      src={project.thumbnail.startsWith('http') ? project.thumbnail : `http://localhost:8000${project.thumbnail}`}
                      alt={project.title}
                      className="card-image"
                    />
                  </div>
                )}
                <Card.Body className="text-end">
                  <Card.Title className="project-title">{project.title}</Card.Title>
                  <Card.Text className="project-description">
                    {project.description.length > 100 
                      ? `${project.description.substring(0, 100)}...` 
                      : project.description}
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
      </Container>
    </div>
  );
};

export default HomePage;