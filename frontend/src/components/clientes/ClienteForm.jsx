import React, { useState, useEffect, useCallback } from 'react';

const Input = React.memo(({ label, name, error, ...rest }) => (
    <div className="flex flex-col">
        <label htmlFor={name} className="mb-1 text-sm font-medium text-gray-600">{label}</label>
        <input
            id={name}
            name={name}
            className={`border p-2 rounded-md w-full ${error ? 'border-red-500 bg-red-50' : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500'}`}
            {...rest}
        />
        {error && <p className="text-red-500 text-xs mt-1">{error}</p>}
    </div>
));

const Select = React.memo(({ label, name, error, options, ...rest }) => (
    <div className="flex flex-col">
        <label htmlFor={name} className="mb-1 text-sm font-medium text-gray-600">{label}</label>
        <select
            id={name}
            name={name}
            className={`border p-2 rounded-md w-full ${error ? 'border-red-500 bg-red-50' : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500'}`}
            {...rest}
        >
            {options.map(option => (
                <option key={option.value} value={option.value}>{option.label}</option>
            ))}
        </select>
        {error && <p className="text-red-500 text-xs mt-1">{error}</p>}
    </div>
));

const Textarea = React.memo(({ label, name, error, ...rest }) => (
    <div className="flex flex-col">
        <label htmlFor={name} className="mb-1 text-sm font-medium text-gray-600">{label}</label>
        <textarea
            id={name}
            name={name}
            rows="3"
            className={`border p-2 rounded-md w-full ${error ? 'border-red-500 bg-red-50' : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500'}`}
            {...rest}
        />
        {error && <p className="text-red-500 text-xs mt-1">{error}</p>}
    </div>
));

const ClienteForm = ({ cliente, onSubmit, onCancel, onClose, apiErrors }) => {
    const [formData, setFormData] = useState({
        // Campos de PessoaBase
        nome: '',
        nuit: '',
        tipoDeIdentificacao: '',
        numeroDeIdentificacao: '',
        residencia: '',
        email: '',
        localDeTrabalho: '',
        telefone: '',
        telefone1: '',
        telefone2: '',
        estadoCivil: '',
        dataDeExpiracao: '',
        dataDeEmissao: '',
        
        // Campos específicos de Cliente
        codigo: '',
        nomeDoArquivoDeIdentificacao: '',
        nacionalidade: '',
        dataDeNascimento: '',
        profissao: '',
        genero: '',
        classificacao: 'medio',
        ativo: true,
        emDivida: false,
        totalEmDivida: 0,
        assinantes: []
    });

    const [errors, setErrors] = useState({});
    const [touched, setTouched] = useState({});

    // Carrega os dados do cliente quando disponível
    useEffect(() => {
        if (cliente) {
            setFormData(prevData => ({
                ...prevData,
                ...cliente,
                // Garantir que campos opcionais não sejam undefined
                email: cliente.email || '',
                nuit: cliente.nuit || '',
                residencia: cliente.residencia || '',
                dataDeNascimento: cliente.dataDeNascimento || '',
                nacionalidade: cliente.nacionalidade || '',
                profissao: cliente.profissao || '',
                assinantes: cliente.assinantes || []
            }));
        }
    }, [cliente]);

    // Atualiza erros quando recebidos da API
    useEffect(() => {
        if (apiErrors) {
            setErrors(prevErrors => ({ ...prevErrors, ...apiErrors }));
        }
    }, [apiErrors]);

    const handleChange = useCallback((e) => {
        const { name, value, type, checked } = e.target;
        const fieldValue = type === 'checkbox' ? checked : value;

        setFormData(prev => ({ ...prev, [name]: fieldValue }));
        
        if (touched[name]) {
            const error = validateField(name, fieldValue);
            setErrors(prev => ({ ...prev, [name]: error }));
        }
    }, [touched]);

    const handleBlur = useCallback((e) => {
        const { name, value } = e.target;
        setTouched(prev => ({ ...prev, [name]: true }));
        const error = validateField(name, value);
        setErrors(prev => ({ ...prev, [name]: error }));
    }, []);

    // ... (seus useEffect permanecem)

    const validateField = useCallback((name, value) => {
        switch (name) {
            case 'nome':
                if (!value) return 'O nome é obrigatório';
                return '';
            
            case 'nuit':
                if (value && !/^\d{9}$/.test(value)) return 'O NUIT deve ter 9 dígitos';
                return '';

            case 'tipoDeIdentificacao':
                if (!value) return 'O tipo de identificação é obrigatório';
                if (!['BI', 'DIRE', 'Passaporte', 'Outro'].includes(value))
                    return 'Tipo de identificação inválido';
                return '';

            case 'numeroDeIdentificacao':
                if (!value) return 'O número de identificação é obrigatório';
                return '';

            case 'telefone':
                if (!value) return 'O telefone é obrigatório';
                if (!/^\d{9,13}$/.test(value.replace(/[^0-9]/g, '')))
                    return 'O telefone deve ter entre 9 e 13 dígitos';
                return '';

            case 'email':
                if (value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value))
                    return 'Email inválido';
                return '';

            case 'genero':
                if (!value) return 'O gênero é obrigatório';
                if (!['masculino', 'feminino', 'transgenero', 'nao-binario', 'agenero', 'pangenero', 'genderqueer', 'two-spirit', 'outro'].includes(value))
                    return 'Gênero inválido';
                return '';

            default:
                return '';
        }
    }, []);

    const validateForm = () => {
        const newErrors = {};
        let isValid = true;

        // Validar campos obrigatórios
        const requiredFields = ['nome', 'tipoDeIdentificacao', 'numeroDeIdentificacao', 'telefone', 'genero'];
        for (const field of requiredFields) {
            const error = validateField(field, formData[field]);
            if (error) {
                newErrors[field] = error;
                isValid = false;
            }
        }

        // Validar campos opcionais se tiverem valor
        const optionalFields = ['nuit', 'email', 'residencia', 'dataDeNascimento', 'nacionalidade', 'profissao'];
        for (const field of optionalFields) {
            if (formData[field]) {
                const error = validateField(field, formData[field]);
                if (error) {
                    newErrors[field] = error;
                    isValid = false;
                }
            }
        }

        setErrors(newErrors);
        return isValid;
    };

    const formatPhoneNumber = (phone) => {
        // Remove qualquer caractere que não seja número
        return phone.replace(/[^0-9]/g, '');
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        // Marca todos os campos como tocados para mostrar todos os erros
        const allTouched = Object.keys(formData).reduce((acc, key) => {
            acc[key] = true;
            return acc;
        }, {});
        setTouched(allTouched);

        if (!validateForm()) {
            return;
        }

        // Prepara os dados para envio
        const formattedData = {
            // Campos obrigatórios
            nome: formData.nome.trim(),
            tipoDeIdentificacao: formData.tipoDeIdentificacao,
            numeroDeIdentificacao: formData.numeroDeIdentificacao.trim(),
            telefone: formatPhoneNumber(formData.telefone),
            genero: formData.genero,
            
            // Campos opcionais (null se vazios)
            email: formData.email?.trim() || null,
            nuit: formData.nuit?.trim() || null,
            residencia: formData.residencia?.trim() || null,
            codigo: formData.codigo?.trim() || null,
            nomeDoArquivoDeIdentificacao: formData.nomeDoArquivoDeIdentificacao?.trim() || null,
            localDeTrabalho: formData.localDeTrabalho?.trim() || null,
            telefone1: formData.telefone1?.trim() || null,
            telefone2: formData.telefone2?.trim() || null,
            estadoCivil: formData.estadoCivil || null,
            dataDeExpiracao: formData.dataDeExpiracao || null,
            dataDeEmissao: formData.dataDeEmissao || null,
            dataDeNascimento: formData.dataDeNascimento || null,
            nacionalidade: formData.nacionalidade?.trim() || null,
            profissao: formData.profissao?.trim() || null,
            
            // Outros campos
            classificacao: formData.classificacao || 'medio',
            ativo: formData.ativo ?? true,
            emDivida: formData.emDivida ?? false,
            totalEmDivida: parseFloat(formData.totalEmDivida || 0),
            
            // Campo assinantes (lista vazia por padrão)
            assinantes: formData.assinantes || []
        };

        // Log para debug
        console.log('Dados a serem enviados:', formattedData);

        console.log('Dados validados e formatados:', formattedData);
        onSubmit(formattedData);
    };

    // ATUALIZAR as opções do Select para tipoDeIdentificacao
    const tipoIdentificacaoOptions = [
        { value: '', label: 'Selecione...' },
        { value: 'BI', label: 'BI' },
        { value: 'Passaporte', label: 'Passaporte' },
        { value: 'Carta de conducao', label: 'Carta de condução' },
        { value: 'Outro', label: 'Outro' }
    ];

    const generoOptions = [
        { value: '', label: 'Selecione...' },
        { value: 'masculino', label: 'Masculino' },
        { value: 'feminino', label: 'Feminino' },
        { value: 'transgenero', label: 'Transgênero' },
        { value: 'nao-binario', label: 'Não-binário' },
        { value: 'agenero', label: 'Agênero' },
        { value: 'pangenero', label: 'Pangênero' },
        { value: 'genderqueer', label: 'Genderqueer' },
        { value: 'two-spirit', label: 'Two-Spirit' },
        { value: 'outro', label: 'Outro' }
    ];

    const estadoCivilOptions = [
        { value: '', label: 'Selecione...' },
        { value: 'Solteiro', label: 'Solteiro' },
        { value: 'Solteira', label: 'Solteira' },
        { value: 'Casado', label: 'Casado' },
        { value: 'Casada', label: 'Casada' },
        { value: 'Separado Judicialmente', label: 'Separado Judicialmente' },
        { value: 'Separada Judicialmente', label: 'Separada Judicialmente' },
        { value: 'Outro', label: 'Outro' }
    ];

    const classificacaoOptions = [
        { value: '', label: 'Selecione...' },
        { value: 'excelente', label: 'Excelente' },
        { value: 'bom', label: 'Bom' },
        { value: 'medio', label: 'Médio' },
        { value: 'mau', label: 'Mau' },
        { value: 'pessimo', label: 'Péssimo' }
    ];

    return (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-xl shadow-2xl w-full max-w-3xl max-h-[90vh] overflow-y-auto">
                {/* ... (cabeçalho) */}

                <form onSubmit={handleSubmit} className="p-6 space-y-8">
                    {/* ... (erro geral) */}

                    {/* Seção: Identificação */}
                    <div className="bg-white p-6 rounded-lg border border-gray-200">
                        <h3 className="text-lg font-semibold text-gray-700 mb-4">Identificação</h3>
                        <div className="space-y-6">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <Input
                                    label="Nome Completo"
                                    name="nome"
                                    value={formData.nome}
                                    onChange={handleChange}
                                    onBlur={handleBlur}
                                    error={errors.nome}
                                    required
                                    placeholder="Nome completo do cliente"
                                />
                                <Input
                                    label="Código do Cliente"
                                    name="codigo"
                                    value={formData.codigo}
                                    onChange={handleChange}
                                    onBlur={handleBlur}
                                    error={errors.codigo}
                                    placeholder="Código único do cliente"
                                />
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <Input
                                    label="NUIT"
                                    name="nuit"
                                    value={formData.nuit}
                                    onChange={handleChange}
                                    onBlur={handleBlur}
                                    error={errors.nuit}
                                    placeholder="000000000"
                                    inputMode="numeric"
                                    maxLength="9"
                                />
                                <Select
                                    label="Tipo de Identificação"
                                    name="tipoDeIdentificacao"
                                    value={formData.tipoDeIdentificacao}
                                    onChange={handleChange}
                                    onBlur={handleBlur}
                                    error={errors.tipoDeIdentificacao}
                                    options={tipoIdentificacaoOptions}
                                    required
                                />
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <Input
                                    label="Número de Identificação"
                                    name="numeroDeIdentificacao"
                                    value={formData.numeroDeIdentificacao}
                                    onChange={handleChange}
                                    onBlur={handleBlur}
                                    error={errors.numeroDeIdentificacao}
                                    required
                                    placeholder="Número do documento"
                                />
                                <Input
                                    label="Nome do Arquivo de Identificação"
                                    name="nomeDoArquivoDeIdentificacao"
                                    value={formData.nomeDoArquivoDeIdentificacao}
                                    onChange={handleChange}
                                    onBlur={handleBlur}
                                    error={errors.nomeDoArquivoDeIdentificacao}
                                    placeholder="Nome do arquivo do documento"
                                />
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <Input
                                    label="Data de Emissão"
                                    name="dataDeEmissao"
                                    type="date"
                                    value={formData.dataDeEmissao}
                                    onChange={handleChange}
                                    onBlur={handleBlur}
                                    error={errors.dataDeEmissao}
                                />
                                <Input
                                    label="Data de Expiração"
                                    name="dataDeExpiracao"
                                    type="date"
                                    value={formData.dataDeExpiracao}
                                    onChange={handleChange}
                                    onBlur={handleBlur}
                                    error={errors.dataDeExpiracao}
                                />
                            </div>
                        </div>
                    </div>

                    {/* Seção: Contato */}
                    <div className="bg-white p-6 rounded-lg border border-gray-200">
                        <h3 className="text-lg font-semibold text-gray-700 mb-4">Contato</h3>
                        <div className="space-y-6">
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                                <Input
                                    label="Telefone Principal"
                                    name="telefone"
                                    value={formData.telefone}
                                    onChange={handleChange}
                                    onBlur={handleBlur}
                                    error={errors.telefone}
                                    required
                                    placeholder="Ex: 841234567"
                                />
                                <Input
                                    label="Telefone Alternativo 1"
                                    name="telefone1"
                                    value={formData.telefone1}
                                    onChange={handleChange}
                                    onBlur={handleBlur}
                                    error={errors.telefone1}
                                    placeholder="Ex: 851234567"
                                />
                                <Input
                                    label="Telefone Alternativo 2"
                                    name="telefone2"
                                    value={formData.telefone2}
                                    onChange={handleChange}
                                    onBlur={handleBlur}
                                    error={errors.telefone2}
                                    placeholder="Ex: 861234567"
                                />
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <Input
                                    label="Email"
                                    name="email"
                                    type="email"
                                    value={formData.email}
                                    onChange={handleChange}
                                    onBlur={handleBlur}
                                    error={errors.email}
                                    placeholder="exemplo@dominio.com"
                                />
                                <Input
                                    label="Local de Trabalho"
                                    name="localDeTrabalho"
                                    value={formData.localDeTrabalho}
                                    onChange={handleChange}
                                    onBlur={handleBlur}
                                    error={errors.localDeTrabalho}
                                    placeholder="Onde trabalha"
                                />
                            </div>

                            <Textarea
                                label="Residência"
                                name="residencia"
                                value={formData.residencia}
                                onChange={handleChange}
                                onBlur={handleBlur}
                                error={errors.residencia}
                                placeholder="Endereço completo"
                            />
                        </div>
                    </div>

                    {/* Seção: Dados Pessoais */}
                    <div className="bg-white p-6 rounded-lg border border-gray-200">
                        <h3 className="text-lg font-semibold text-gray-700 mb-4">Dados Pessoais</h3>
                        <div className="space-y-6">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <Input
                                    label="Data de Nascimento"
                                    name="dataDeNascimento"
                                    type="date"
                                    value={formData.dataDeNascimento}
                                    onChange={handleChange}
                                    onBlur={handleBlur}
                                    error={errors.dataDeNascimento}
                                />
                                <Input
                                    label="Nacionalidade"
                                    name="nacionalidade"
                                    value={formData.nacionalidade}
                                    onChange={handleChange}
                                    onBlur={handleBlur}
                                    error={errors.nacionalidade}
                                    placeholder="Ex: Moçambicana"
                                />
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <Select
                                    label="Gênero"
                                    name="genero"
                                    value={formData.genero}
                                    onChange={handleChange}
                                    onBlur={handleBlur}
                                    error={errors.genero}
                                    options={generoOptions}
                                    required
                                />
                                <Select
                                    label="Estado Civil"
                                    name="estadoCivil"
                                    value={formData.estadoCivil}
                                    onChange={handleChange}
                                    onBlur={handleBlur}
                                    error={errors.estadoCivil}
                                    options={estadoCivilOptions}
                                />
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <Input
                                    label="Profissão"
                                    name="profissao"
                                    value={formData.profissao}
                                    onChange={handleChange}
                                    onBlur={handleBlur}
                                    error={errors.profissao}
                                    placeholder="Profissão atual"
                                />
                                <Select
                                    label="Classificação"
                                    name="classificacao"
                                    value={formData.classificacao}
                                    onChange={handleChange}
                                    onBlur={handleBlur}
                                    error={errors.classificacao}
                                    options={classificacaoOptions}
                                />
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="flex items-center space-x-2">
                                    <input
                                        type="checkbox"
                                        id="ativo"
                                        name="ativo"
                                        checked={formData.ativo}
                                        onChange={handleChange}
                                        className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                                    />
                                    <label htmlFor="ativo" className="text-sm font-medium text-gray-700">
                                        Cliente Ativo
                                    </label>
                                </div>
                                <div className="flex items-center space-x-2">
                                    <input
                                        type="checkbox"
                                        id="emDivida"
                                        name="emDivida"
                                        checked={formData.emDivida}
                                        onChange={handleChange}
                                        className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                                    />
                                    <label htmlFor="emDivida" className="text-sm font-medium text-gray-700">
                                        Em Dívida
                                    </label>
                                </div>
                            </div>

                            {formData.emDivida && (
                                <Input
                                    label="Total em Dívida"
                                    name="totalEmDivida"
                                    type="number"
                                    value={formData.totalEmDivida}
                                    onChange={handleChange}
                                    onBlur={handleBlur}
                                    error={errors.totalEmDivida}
                                    placeholder="0.00"
                                    step="0.01"
                                    min="0"
                                />
                            )}
                        </div>
                    </div>

                    {/* CAMPO OCULTO para assinantes (obrigatório) */}
                    <input 
                        type="hidden" 
                        name="assinantes" 
                        value={JSON.stringify(formData.assinantes)} 
                    />

                    {/* Ações */}
                    <div className="flex justify-end gap-3 pt-6 border-t">
                        <button
                            type="button"
                            onClick={onCancel}
                            className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
                        >
                            Cancelar
                        </button>
                        <button
                            type="submit"
                            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
                        >
                            Salvar
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default ClienteForm;