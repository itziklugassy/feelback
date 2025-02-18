import React, { useState, useEffect } from 'react';
import { Container, Card, Alert } from 'react-bootstrap';  
import { useParams, useNavigate } from 'react-router-dom';
import { getProject, submitRating, isAuthenticated } from '../services/api';
import './ProjectPage.css'; 

const ProjectPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [project, setProject] = useState(null);
  const [ratings, setRatings] = useState({
    insight_score: 0,
    concept_score: 0,
    execution_score: 0,
    prominence_score: 0,
    pride_score: 0,
    originality_score: 0
  });
  const [message, setMessage] = useState(null);
  const [loading, setLoading] = useState(false);

  const getYouTubeEmbedUrl = (url) => {
    if (!url) return null;
    const videoId = url.split('v=')[1];
    if (!videoId) return null;
    return `https://www.youtube.com/embed/${videoId}`;
  };

  useEffect(() => {
    const fetchProject = async () => {
      try {
        const data = await getProject(id);
        setProject(data);
      } catch (error) {
        console.error('Error fetching project:', error);
        setMessage({ type: 'danger', text: 'שגיאה בטעינת הפרויקט' });
      }
    };

    fetchProject();
  }, [id]);

  const handleRatingChange = (field, value) => {
    setRatings(prev => ({
      ...prev,
      [field]: parseInt(value)
    }));
  };

  const handleSubmit = async () => {
    if (!isAuthenticated()) {
      navigate('/login');
      return;
    }
    
    setLoading(true);
    try {
      await submitRating(project.id, ratings);
      setMessage({ type: 'success', text: 'הדירוג נשלח בהצלחה!' });
      setTimeout(() => setMessage(null), 3000);
    } catch (error) {
      setMessage({ type: 'danger', text: 'שגיאה בשליחת הדירוג' });
    }
    setLoading(false);
  };

  const RatingBar = ({ label, field, value }) => (
    <div className="rating-item">
      <div className="rating-header">
        <span className="rating-value">{value}</span>
        <label className="rating-label">{label}</label>
      </div>
      <input 
        type="range" 
        className="range-slider"
        min="0" 
        max="10" 
        value={value}
        onChange={(e) => handleRatingChange(field, e.target.value)}
      />
    </div>
  );

  if (!project) return <div className="loading-screen">טוען...</div>;

  return (
    <div className="project-page">
      <Container>
      <nav aria-label="breadcrumb" className="breadcrumb-nav">
  <ol className="breadcrumb">
    <li className="breadcrumb-item">
      <span className="x-separator" style={{ color: '#da009d', fontWeight: 'bold', marginLeft: '5px' }}>X</span>
      <a href="/">דף הבית</a>
    </li>
    <li className="breadcrumb-item active">
      <span className="x-separator" style={{ color: '#da009d', fontWeight: 'bold', marginLeft: '5px' }}>X</span>
      {project.title}
    </li>
  </ol>
</nav>

        {message && (
          <Alert variant={message.type} className="alert-message">
            {message.text}
          </Alert>
        )}

        <div className="project-header">
          <h1 className="project-title">{project.title}</h1>
        </div>

        <div className="project-content">
          <Card className="description-card">
            <Card.Body>
              <p className="project-description">{project.description}</p>
            </Card.Body>
          </Card>

          {project.media_url && (
            <div className="video-container">
              <div className="ratio ratio-16x9">
                <iframe
                  src={getYouTubeEmbedUrl(project.media_url)}
                  title={project.title}
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                  className="video-frame"
                />
              </div>
            </div>
          )}

          <Card className="rating-card">
            <Card.Body>
              <h3 className="rating-section-title">דירוג הפרויקט</h3>
              <div className="rating-bars">
                <RatingBar label="תובנה" field="insight_score" value={ratings.insight_score} />
                <RatingBar label="קונספט" field="concept_score" value={ratings.concept_score} />
                <RatingBar label="ביצוע" field="execution_score" value={ratings.execution_score} />
                <RatingBar label="בולטות" field="prominence_score" value={ratings.prominence_score} />
                <RatingBar label="גאווה" field="pride_score" value={ratings.pride_score} />
                <RatingBar label="מקוריות" field="originality_score" value={ratings.originality_score} />
                <button 
                  className="submit-button"
                  onClick={handleSubmit}
                  disabled={loading}
                >
                  {loading ? 'שולח...' : 'שלח דירוג'}
                </button>
              </div>
            </Card.Body>
          </Card>
        </div>
      </Container>
    </div>
  );
};

export default ProjectPage;