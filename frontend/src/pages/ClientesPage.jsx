import React, { useState, useEffect } from 'react';
import ClienteForm from '../components/clientes/ClienteForm';
import ClienteList from '../components/clientes/ClienteList';
import api from '../services/api';
import Sidebar from '../components/shared/Sidebar';

const ClientesPage = () => {

    const [showForm, setShowForm] = useState(false);
    const [editingCliente, setEditingCliente] = useState(null);
    const [clientes, setClientes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [formErrors, setFormErrors] = useState(null); // Estado para erros do formulário

    // Carrega os clientes do backend
    const loadClientes = async () => {
        try {
            console.log('Carregando clientes...');
            const response = await api.get('clientes/');
            console.log('Clientes carregados:', response.data);
            setClientes(response.data);
            setLoading(false);
        } catch (err) {
            console.error('Erro ao buscar clientes:', err);
            console.error('Detalhes do erro:', err.response?.data);
            setError('Não foi possível carregar os clientes');
            setLoading(false);
        }
    };

    useEffect(() => {
        loadClientes();
    }, []);

    // Abre o formulário para novo cliente
    const handleNovoCliente = () => {
        setFormErrors(null); // Limpa erros ao abrir novo formulário

        // Gera um código único de 4 dígitos para o novo cliente
        let novoCodigo;
        let isUnique = false;
        while (!isUnique) {
            // Gera um número aleatório de 1000 a 9999
            novoCodigo = Math.floor(1000 + Math.random() * 9000).toString();
            // Verifica se o código já existe na lista de clientes
            const codigoExistente = clientes.some(c => c.codigo === novoCodigo);
            if (!codigoExistente) {
                isUnique = true;
            }
        }

        // Define o estado de edição com o novo código
        setEditingCliente({
            codigo: novoCodigo,
            // O ClienteForm já lida com os campos vazios, então você só precisa do 'codigo'.
        });
        
        setShowForm(true);
    };

    // Fecha o formulário
    const handleCloseForm = () => {
        setShowForm(false);
        setEditingCliente(null);
        setError('');
        setFormErrors(null); // Limpa erros ao fechar
    };

    // Submete novo cliente ou edição
    const handleSubmitCliente = async (formData) => {
        try {
            setFormErrors(null); // Limpa erros anteriores
            console.log('✅ Dados validados no frontend:', formData);

            // Validação final antes de enviar
            if (!formData.nome || !formData.nome.trim()) {
                setFormErrors({ form: 'Nome é obrigatório' });
                return;
            }

            if (editingCliente&& editingCliente.id) {
                console.log('Editando cliente ID:', editingCliente.id);
                const response = await api.put(`clientes/${editingCliente.id}/`, formData);
                console.log('Resposta da edição:', response.data);

                const clienteAtualizado = response.data;
                setClientes(prev =>
                    prev.map(c => (c.id === clienteAtualizado.id ? clienteAtualizado : c))
                );
            } else {
                const response = await api.post('clientes/', formData);
                console.log('Resposta da criação:', response.data);

                setClientes(prev => [...prev, response.data]);
            }
            handleCloseForm();
        } catch (err) {
            console.error('Erro completo ao salvar cliente:', err);
            console.error('Resposta do erro:', err.response?.data);

            // Mostra erro específico do backend
            const backendError = err.response?.data;
            if (backendError && typeof backendError === 'object') {
                setFormErrors(backendError); // Passa os erros de campo para o formulário
            } else {
                const errorMessage = backendError?.message || 'Não foi possível salvar o cliente';
                setFormErrors({ form: errorMessage }); // Erro geral para o formulário
            }
        }
    };

    // Edita cliente existente
    const handleEditCliente = (cliente) => {
        console.log('Editando cliente:', cliente);
        setEditingCliente(cliente);
        setFormErrors(null); // Limpa erros ao abrir para edição
        setShowForm(true);
    };

    // Exclui cliente
    const handleDeleteCliente = async (id) => {
        if (!window.confirm('Tem certeza que deseja excluir este cliente?')) {
            return;
        }

        try {
            console.log('Excluindo cliente ID:', id);
            await api.delete(`clientes/${id}/`);
            setClientes(prev => prev.filter(c => c.id !== id));
        } catch (err) {
            console.error('Erro ao excluir cliente:', err);
            console.error('Resposta do erro:', err.response?.data);
            setError('Não foi possível excluir o cliente');
        }
    };

    return (
        
        <div className="p-6 max-w-6xl mx-auto">
            
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-bold text-gray-800">📋 Lista de clientes</h1>
                <button
                    onClick={handleNovoCliente}
                    className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
                >
                    + Novo Cliente
                </button>
            </div>

            {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                    {error}
                    <button
                        onClick={() => setError('')}
                        className="float-right text-red-800 hover:text-red-900"
                    >
                        ×
                    </button>
                </div>
            )}

            {showForm ? (
                <ClienteForm
                    cliente={editingCliente}
                    onSubmit={handleSubmitCliente}
                    onCancel={handleCloseForm}
                    onClose={handleCloseForm}
                    apiErrors={formErrors}
                />
            ) : loading ? (
                <div className="text-center py-8">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                    <p className="mt-2 text-gray-600">Carregando clientes...</p>
                </div>
            ) : !error && (
                <ClienteList
                    clientes={clientes}
                    onEdit={handleEditCliente}
                    onDelete={handleDeleteCliente}
                />
            )}
        </div>
    );
};

export default ClientesPage;