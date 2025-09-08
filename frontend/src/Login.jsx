import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(false);

    // ⭐ Use o useNavigate do React Router DOM para redirecionamento
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setMessage('');

        try {
            // ⭐ A requisição agora aponta para a URL do token do Simple JWT
            const response = await fetch('/api/token/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password })
            });

            if (response.ok) {
                const data = await response.json();

                // Limpa tokens antigos
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');

                // Salva os novos tokens
                localStorage.setItem('access_token', data.access);
                localStorage.setItem('refresh_token', data.refresh);

                setMessage('✅ Login bem-sucedido!');

                // Redireciona o usuário para a página principal
                navigate('/');

            } else {
                // Se a resposta não for OK, tenta pegar a mensagem de erro
                const errorData = await response.json();
                const errorMessage = errorData.detail || 'Credenciais inválidas.';
                setMessage('❌ Erro: ' + errorMessage);
            }

        } catch (error) {
            console.error('⭐ Erro de conexão:', error);
            setMessage('⚠️ Erro de conexão. Verifique se o servidor está online.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ padding: '20px', maxWidth: '400px', margin: '0 auto' }}>
            <h2>🔐 Login</h2>

            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: '15px' }}>
                    <label>Usuário:</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                        disabled={loading}
                        placeholder="Digite seu username"
                    />
                </div>

                <div style={{ marginBottom: '15px' }}>
                    <label>Senha:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        disabled={loading}
                        placeholder="Digite sua senha"
                    />
                </div>

                <button type="submit" disabled={loading}>
                    {loading ? '⏳ Processando...' : 'Entrar'}
                </button>
            </form>

            {message && (
                <div style={{
                    marginTop: '15px',
                    padding: '10px',
                    backgroundColor: message.includes('✅') ? '#d4edda' : '#f8d7da',
                    color: message.includes('✅') ? '#155724' : '#721c24'
                }}>
                    <strong>{message}</strong>
                </div>
            )}
        </div>
    );
};

export default Login;