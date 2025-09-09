import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Sidebar = ({ isOpen, onClose }) => {
    const location = useLocation();

    const menuItems = [
        { path: '/dashboard', label: 'Dashboard', icon: '📊' },
        { path: '/clientes', label: 'Clientes', icon: '👥' },
        { path: '/assinantes', label: 'Assinantes', icon: '📝' },
    ];

    const isActive = (path) => location.pathname === path;

    return (
        <>
            {/* Overlay para mobile */}
            {isOpen && (
                <div
                    className="fixed inset-0 bg-gray-900 bg-opacity-50 z-20 lg:hidden"
                    onClick={onClose}
                />
            )}

            {/* Sidebar */}
            <div className={`
                fixed inset-y-0 left-0 z-30 w-64 bg-blue-900 text-white 
                transform transition-transform duration-300 ease-in-out
                lg:static lg:translate-x-0
                ${isOpen ? 'translate-x-0' : '-translate-x-full'}
            `}>
                <div className="flex flex-col items-center justify-center p-4 border-b border-blue-800">
                    {/* Logo no topo de tudo */}
                    <img 
                        src="/src/assets/images/logo.png" 
                        alt="Logo MALEYANGA" 
                        className="h-16 w-16 mb-2" // Tamanho maior para destaque
                        onError={(e) => {
                            // Fallback se a imagem não carregar
                            e.target.style.display = 'none';
                            // Mostra texto alternativo
                            const fallback = document.createElement('h1');
                            fallback.className = 'text-xl font-semibold';
                            fallback.textContent = 'MALEYANGA';
                            e.target.parentNode.appendChild(fallback);
                        }}
                    />
                    <button onClick={onClose} className="lg:hidden absolute top-4 right-4">
                        ✕
                    </button>
                </div>

                <nav className="p-4">
                    <ul className="space-y-2">
                        {menuItems.map((item) => (
                            <li key={item.path}>
                                <Link
                                    to={item.path}
                                    className={`
                                        flex items-center p-3 rounded-lg transition-colors
                                        ${isActive(item.path)
                                        ? 'bg-blue-800 text-white'
                                        : 'text-blue-200 hover:bg-blue-800 hover:text-white'
                                    }
                                    `}
                                    onClick={onClose}
                                >
                                    <span className="mr-3">{item.icon}</span>
                                    <span>{item.label}</span>
                                </Link>
                            </li>
                        ))}
                    </ul>

                    {/* Logout */}
                    <div className="mt-8 pt-4 border-t border-blue-800">
                        <button
                            onClick={() => {
                                localStorage.removeItem('access_token');
                                localStorage.removeItem('refresh_token');
                                window.location.href = '/login';
                            }}
                            className="flex items-center p-3 rounded-lg text-blue-200 hover:bg-blue-800 hover:text-white w-full"
                        >
                            <span className="mr-3">🚪</span>
                            <span>Sair</span>
                        </button>
                    </div>
                </nav>
            </div>
        </>
    );
};

export default Sidebar;