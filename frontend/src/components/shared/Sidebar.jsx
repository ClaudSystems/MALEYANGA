import React from 'react';
import { Link, useLocation } from 'react-router-dom';

// Sistema de rota automática - adicione novas páginas aqui
const appRoutes = {
  '/dashboard': { label: 'Dashboard', icon: '📊', category: 'main' },
  '/clientes': { label: 'Clientes', icon: '👥', category: 'main' },
  '/creditos': { label: 'Créditos', icon: '💰', category: 'main' },
  '/assinantes': { label: 'Assinantes', icon: '📝', category: 'main' },
  '/pagamentos': { label: 'Pagamentos', icon: '💳', category: 'financeiro' },
  '/relatorios': { label: 'Relatórios', icon: '📈', category: 'financeiro' },
  // Adicione novas rotas aqui automaticamente
};

const Sidebar = ({ isOpen, onClose }) => {
    const location = useLocation();

    // Agrupar rotas por categoria
    const groupedRoutes = Object.entries(appRoutes).reduce((acc, [path, data]) => {
        const category = data.category || 'outros';
        if (!acc[category]) {
            acc[category] = [];
        }
        acc[category].push({ path, ...data });
        return acc;
    }, {});

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
                    <img 
                        src="/src/assets/images/logo.png" 
                        alt="Logo MALEYANGA" 
                        className="h-16 w-16 mb-2"
                        onError={(e) => {
                            e.target.style.display = 'none';
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
                    {/* Menu Principal */}
                    <div className="mb-6">
                        <h3 className="text-blue-400 text-xs uppercase font-semibold mb-3 pl-3">
                            Principal
                        </h3>
                        <ul className="space-y-2">
                            {groupedRoutes.main?.map((item) => (
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
                    </div>

                    {/* Outras Categorias */}
                    {Object.entries(groupedRoutes).map(([category, routes]) => {
                        if (category === 'main') return null;
                        
                        return (
                            <div key={category} className="mb-6">
                                <h3 className="text-blue-400 text-xs uppercase font-semibold mb-3 pl-3">
                                    {category.charAt(0).toUpperCase() + category.slice(1)}
                                </h3>
                                <ul className="space-y-2">
                                    {routes.map((item) => (
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
                            </div>
                        );
                    })}

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