/**
 * API Service
 * Handles all backend API communication
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Check backend health
 */
export const checkHealth = async () => {
  const response = await api.get('/api/health');
  return response.data;
};

/**
 * Get available disease classes
 */
export const getClasses = async () => {
  const response = await api.get('/api/classes');
  return response.data;
};

/**
 * Get model information
 */
export const getModelInfo = async () => {
  const response = await api.get('/api/model/info');
  return response.data;
};

/**
 * Predict disease from image
 * @param {File} imageFile - Image file to analyze
 */
export const predictDisease = async (imageFile) => {
  const formData = new FormData();
  formData.append('file', imageFile);

  const response = await api.post('/api/predict', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export default {
  checkHealth,
  getClasses,
  getModelInfo,
  predictDisease,
};
