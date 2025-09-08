// src/utils/apiTest.js
import api from '../services/api';

export const testClienteAPI = async () => {
    try {
        console.log('=== TESTANDO API CLIENTES ===');

        // Teste de GET
        console.log('Testando GET /clientes/');
        const getResponse = await api.get('clientes/');
        console.log('GET Response:', getResponse.data);

        // Teste de POST (se necessário)
        const testData = {
            nome: "Cliente Teste",
            telefone: "+258841234567",
            email: "teste@email.com",
            ativo: true
        };

        console.log('Testando POST /clientes/');
        const postResponse = await api.post('clientes/', testData);
        console.log('POST Response:', postResponse.data);

        return true;
    } catch (error) {
        console.error('Erro no teste da API:', error);
        console.error('Status:', error.response?.status);
        console.error('Data:', error.response?.data);
        console.error('URL:', error.config?.url);
        return false;
    }
};

// Execute no console do navegador para testar:
// testClienteAPI();
