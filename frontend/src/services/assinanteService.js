import api from './api';

export const assinanteService = {
    getAll: () => api.get('/assinantes/'),
    getById: (id) => api.get(`/assinantes/${id}/`),
    create: (data) => api.post('/assinantes/', data),
    update: (id, data) => api.put(`/assinantes/${id}/`, data),
    delete: (id) => api.delete(`/assinantes/${id}/`),
    getByCliente: (clienteId) => api.get(`/assinantes/?cliente=${clienteId}`),
};