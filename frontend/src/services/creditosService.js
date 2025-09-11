// services/creditosService.js
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const creditosService = {
  getCreditos: () => axios.get(`${API_BASE_URL}/creditos/`),
  getCredito: (id) => axios.get(`${API_BASE_URL}/creditos/${id}/`),
  createCredito: (data) => axios.post(`${API_BASE_URL}/creditos/`, data),
  updateCredito: (id, data) => axios.put(`${API_BASE_URL}/creditos/${id}/`, data),
  deleteCredito: (id) => axios.delete(`${API_BASE_URL}/creditos/${id}/`),
};