import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para manejo de errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export const surveyAPI = {
  // Subir archivo de encuesta
  uploadSurvey: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/upload-survey', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Realizar análisis
  analyzeSurvey: async (surveyId, analysisTypes) => {
    const response = await api.post('/analyze', {
      survey_id: surveyId,
      analysis_types: analysisTypes,
    });
    return response.data;
  },

  // Obtener insights de IA
  getAIInsights: async (surveyId) => {
    const response = await api.get(`/ai-insights/${surveyId}`);
    return response.data;
  },

  // Obtener visualizaciones
  getVisualizations: async (surveyId, chartTypes = null) => {
    const params = chartTypes ? { chart_types: chartTypes.join(',') } : {};
    const response = await api.get(`/visualizations/${surveyId}`, { params });
    return response.data;
  },

  // Listar encuestas
  listSurveys: async () => {
    const response = await api.get('/surveys');
    return response.data;
  },

  // Eliminar encuesta
  deleteSurvey: async (surveyId) => {
    const response = await api.delete(`/surveys/${surveyId}`);
    return response.data;
  },

  // Verificar estado del servidor
  healthCheck: async () => {
    const response = await api.get('/');
    return response.data;
  },
};

export default api;
