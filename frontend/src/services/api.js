import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

// Helper function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Create axios instance with default config
const api = axios.create({
    baseURL: API_URL,
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
    }
});

// Authentication
export const login = async (credentials) => {
    try {
        const csrfToken = getCookie('csrftoken');
        const response = await api.post('/login/', credentials, {
            headers: {
                'X-CSRFToken': csrfToken,
                // Remove any existing token for login request
                'Authorization': ''
            }
        });
        
        if (response.data.token) {
            localStorage.setItem('token', response.data.token);
            localStorage.setItem('username', response.data.username);
            // Update axios default headers after successful login
            api.defaults.headers.common['Authorization'] = `Token ${response.data.token}`;
        }
        return response.data;
    } catch (error) {
        console.error('Login error:', error);
        if (error.response) {
            // Server responded with error
            throw new Error(error.response.data.detail || 'Login failed');
        } else if (error.request) {
            // Request made but no response
            throw new Error('No response from server');
        } else {
            // Request setup error
            throw new Error('Error setting up request');
        }
    }
};

// Projects
export const getProjects = async () => {
    try {
        const response = await api.get('/projects/');
        return response.data;
    } catch (error) {
        console.error('Error fetching projects:', error);
        if (error.response?.status === 403) {
            // Handle authentication errors
            logout();
        }
        throw new Error(error.response?.data?.detail || 'Failed to fetch projects');
    }
};

export const getProject = async (id) => {
    try {
        const response = await api.get(`/projects/${id}/`);
        return response.data;
    } catch (error) {
        console.error('Error fetching project:', error);
        if (error.response?.status === 403) {
            logout();
        }
        throw new Error(error.response?.data?.detail || 'Failed to fetch project');
    }
};

// Ratings
export const submitRating = async (projectId, ratings) => {
    try {
        const csrfToken = getCookie('csrftoken');
        const response = await api.post('/ratings/', {
            project: projectId,
            ...ratings
        }, {
            headers: {
                'X-CSRFToken': csrfToken
            }
        });
        return response.data;
    } catch (error) {
        console.error('Error submitting rating:', error);
        if (error.response?.status === 403) {
            logout();
        }
        throw new Error(error.response?.data?.detail || 'Failed to submit rating');
    }
};

// Helper functions
export const isAuthenticated = () => {
    const token = localStorage.getItem('token');
    return !!token;
};

export const getUsername = () => {
    return localStorage.getItem('username');
};

export const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    // Clear Authorization header
    delete api.defaults.headers.common['Authorization'];
};

// Add interceptors for request and response
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Token ${token}`;
        }
        // Add CSRF token to all non-GET requests
        if (config.method !== 'get') {
            const csrfToken = getCookie('csrftoken');
            if (csrfToken) {
                config.headers['X-CSRFToken'] = csrfToken;
            }
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor to handle common errors
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401 || error.response?.status === 403) {
            // Handle authentication errors
            logout();
        }
        return Promise.reject(error);
    }
);

export default api;