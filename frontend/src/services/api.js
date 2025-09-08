import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/api/',
});

// Função para renovar o token usando o refresh token
const refreshToken = async () => {
    try {
        const refresh = localStorage.getItem('refresh_token');
        if (!refresh) throw new Error('No refresh token');

        const response = await axios.post('http://localhost:8000/api/token/refresh/', {
            refresh: refresh
        });

        const { access } = response.data;
        localStorage.setItem('access_token', access);
        return access;
    } catch (error) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        throw error;
    }
};

// Interceptor para adicionar o token em todas as requisições
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Interceptor para tratar erros de token expirado
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        // Se o erro for 401 e não for uma tentativa de refresh
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                // Tenta renovar o token
                const newToken = await refreshToken();
                
                // Atualiza o token na requisição original
                originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
                
                // Refaz a requisição original com o novo token
                return api(originalRequest);
            } catch (refreshError) {
                // Se falhar em renovar o token, redireciona para login
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

export default api;