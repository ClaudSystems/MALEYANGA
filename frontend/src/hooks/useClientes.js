import { useState, useEffect } from 'react';
import { clienteService } from '../services/clienteService';

export const useClientes = () => {
    const [clientes, setClientes] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchClientes = async () => {
        try {
            setLoading(true);
            const response = await clienteService.getAll();
            setClientes(response.data);
            setError(null);
        } catch (err) {
            setError('Erro ao carregar clientes');
            console.error('Error fetching clientes:', err);
        } finally {
            setLoading(false);
        }
    };

    const createCliente = async (clienteData) => {
        try {
            const response = await clienteService.create(clienteData);
            setClientes(prev => [...prev, response.data]);
            return response.data;
        } catch (err) {
            setError('Erro ao criar cliente');
            throw err;
        }
    };

    const updateCliente = async (id, clienteData) => {
        try {
            const response = await clienteService.update(id, clienteData);
            setClientes(prev => prev.map(cliente =>
                cliente.id === id ? response.data : cliente
            ));
            return response.data;
        } catch (err) {
            setError('Erro ao atualizar cliente');
            throw err;
        }
    };

    const deleteCliente = async (id) => {
        try {
            await clienteService.delete(id);
            setClientes(prev => prev.filter(cliente => cliente.id !== id));
        } catch (err) {
            setError('Erro ao deletar cliente');
            throw err;
        }
    };

    useEffect(() => {
        fetchClientes();
    }, []);

    return {
        clientes,
        loading,
        error,
        createCliente,
        updateCliente,
        deleteCliente,
        refetch: fetchClientes
    };
};