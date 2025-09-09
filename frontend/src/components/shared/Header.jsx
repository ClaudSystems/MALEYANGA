import React from 'react';

const Header = ({ onMenuClick, pageTitle }) => {
    return (
        <header className="bg-white shadow-sm border-b">
            <div className="flex items-center justify-between p-4">
                <div className="flex items-center">
                    <button
                        onClick={onMenuClick}
                        className="lg:hidden p-2 rounded-md text-gray-600 hover:bg-gray-100"
                    >
                        ☰
                    </button>
                    
                    {/* Logo + Título */}
                    <div className="flex items-center ml-2">
                     
                        <h1 className="text-xl font-semibold text-gray-800">
                            {pageTitle || 'MALEYANGA'}
                        </h1>
                    </div>
                </div>

                <div className="flex items-center space-x-4">
                    <span className="text-sm text-gray-600">
                        Bem-vindo, Administrador
                    </span>
                    <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white text-sm">
                        A
                    </div>
                </div>
            </div>
        </header>
    );
};

export default Header;