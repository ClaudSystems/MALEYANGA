import React, { useState, useEffect } from 'react';
import { useSnackbar } from 'notistack';
import {
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  IconButton,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Switch,
  FormControlLabel,
  Chip,
  Typography
} from '@mui/material';
import {
  Edit as EditIcon,
  Add as AddIcon,
  Check as CheckIcon,
  Close as CloseIcon
} from '@mui/icons-material';
import api from '../services/api';

const TaxasPage = () => {
  const [taxas, setTaxas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingTaxa, setEditingTaxa] = useState(null);
  const [formData, setFormData] = useState({
    nome: '',
    valor: '',
    percentagem: '',
    valor_minimo: '',
    valor_maximo: '',
    recorencia: '',
    entidade: '',
    activo: true
  });
  
  const { enqueueSnackbar } = useSnackbar();

  const recorenciaOptions = [
    { value: 'diaria', label: 'Diária' },
    { value: 'semanal', label: 'Semanal' },
    { value: 'mensal', label: 'Mensal' },
    { value: 'trimestral', label: 'Trimestral' },
    { value: 'semestral', label: 'Semestral' },
    { value: 'anual', label: 'Anual' },
    { value: 'unica', label: 'Única' },
  ];

  useEffect(() => {
    fetchTaxas();
  }, []);

  const fetchTaxas = async () => {
    try {
      setLoading(true);
      const response = await api.get('/taxas/');
      setTaxas(response.data);
    } catch (error) {
      enqueueSnackbar('Erro ao carregar taxas', { variant: 'error' });
      console.error('Erro ao carregar taxas:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenDialog = (taxa = null) => {
    if (taxa) {
      setEditingTaxa(taxa);
      setFormData({
        nome: taxa.nome || '',
        valor: taxa.valor || '',
        percentagem: taxa.percentagem || '',
        valor_minimo: taxa.valor_minimo || '',
        valor_maximo: taxa.valor_maximo || '',
        recorencia: taxa.recorencia || '',
        entidade: taxa.entidade || '',
        activo: taxa.activo
      });
    } else {
      setEditingTaxa(null);
      setFormData({
        nome: '',
        valor: '',
        percentagem: '',
        valor_minimo: '',
        valor_maximo: '',
        recorencia: '',
        entidade: '',
        activo: true
      });
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingTaxa(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        ...formData,
        valor: formData.valor ? parseFloat(formData.valor) : null,
        percentagem: formData.percentagem ? parseFloat(formData.percentagem) : null,
        valor_minimo: formData.valor_minimo ? parseFloat(formData.valor_minimo) : null,
        valor_maximo: formData.valor_maximo ? parseFloat(formData.valor_maximo) : null
      };

      if (editingTaxa) {
        await api.put(`/taxas/${editingTaxa.id}/`, payload);
        enqueueSnackbar('Taxa atualizada com sucesso', { variant: 'success' });
      } else {
        await api.post('/taxas/', payload);
        enqueueSnackbar('Taxa criada com sucesso', { variant: 'success' });
      }
      
      fetchTaxas();
      handleCloseDialog();
    } catch (error) {
      console.error('Erro ao salvar taxa:', error);
      enqueueSnackbar('Erro ao salvar taxa', { variant: 'error' });
    }
  };

  const handleToggleActivo = async (taxa) => {
    try {
      await api.post(`/taxas/${taxa.id}/toggle_activo/`);
      enqueueSnackbar('Estado alterado com sucesso', { variant: 'success' });
      fetchTaxas();
    } catch (error) {
      console.error('Erro ao alterar estado:', error);
      enqueueSnackbar('Erro ao alterar estado', { variant: 'error' });
    }
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const formatCurrency = (value) => {
    if (!value) return '-';
    return new Intl.NumberFormat('pt-MZ', {
      style: 'currency',
      currency: 'MZN'
    }).format(value);
  };

  if (loading) {
    return (
      <Box className="p-6">
        <Typography>Carregando taxas...</Typography>
      </Box>
    );
  }

  return (
    <Box className="p-6 bg-gray-50 min-h-screen">
      {/* Header */}
      <Box className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
        <Typography variant="h4" component="h1" className="font-bold text-gray-800">
          Gestão de Taxas
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
          className="bg-blue-600 hover:bg-blue-700 shadow-md"
        >
          Nova Taxa
        </Button>
      </Box>

      {/* Table */}
      <Paper className="rounded-lg shadow-md overflow-hidden">
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow className="bg-gray-100">
                <TableCell className="font-semibold">Nome</TableCell>
                <TableCell className="font-semibold">Valor</TableCell>
                <TableCell className="font-semibold">Percentagem</TableCell>
                <TableCell className="font-semibold">Recorrência</TableCell>
                <TableCell className="font-semibold">Valor Mínimo</TableCell>
                <TableCell className="font-semibold">Valor Máximo</TableCell>
                <TableCell className="font-semibold">Estado</TableCell>
                <TableCell className="font-semibold">Ações</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {taxas.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={8} align="center" className="py-8 text-gray-500">
                    Nenhuma taxa encontrada
                  </TableCell>
                </TableRow>
              ) : (
                taxas
                  .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                  .map((taxa) => (
                    <TableRow 
                      key={taxa.id} 
                      className="hover:bg-gray-50 transition-colors"
                    >
                      <TableCell className="font-medium">{taxa.nome}</TableCell>
                      <TableCell>{formatCurrency(taxa.valor)}</TableCell>
                      <TableCell>
                        {taxa.percentagem ? (
                          <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-sm">
                            {taxa.percentagem}%
                          </span>
                        ) : (
                          '-'
                        )}
                      </TableCell>
                      <TableCell>
                        {taxa.recorencia ? (
                          <Chip
                            label={
                              recorenciaOptions.find(r => r.value === taxa.recorencia)?.label || taxa.recorencia
                            }
                            size="small"
                            className="bg-purple-100 text-purple-800"
                          />
                        ) : (
                          '-'
                        )}
                      </TableCell>
                      <TableCell>{formatCurrency(taxa.valor_minimo)}</TableCell>
                      <TableCell>{formatCurrency(taxa.valor_maximo)}</TableCell>
                      <TableCell>
                        <Chip
                          icon={taxa.activo ? <CheckIcon /> : <CloseIcon />}
                          label={taxa.activo ? 'Ativa' : 'Inativa'}
                          color={taxa.activo ? 'success' : 'error'}
                          size="small"
                          className={taxa.activo ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}
                        />
                      </TableCell>
                      <TableCell>
                        <div className="flex gap-2">
                          <IconButton
                            size="small"
                            onClick={() => handleOpenDialog(taxa)}
                            className="text-blue-600 hover:bg-blue-50"
                          >
                            <EditIcon />
                          </IconButton>
                          <IconButton
                            size="small"
                            onClick={() => handleToggleActivo(taxa)}
                            className={taxa.activo ? 'text-red-600 hover:bg-red-50' : 'text-green-600 hover:bg-green-50'}
                          >
                            {taxa.activo ? <CloseIcon /> : <CheckIcon />}
                          </IconButton>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
        
        {taxas.length > 0 && (
          <TablePagination
            rowsPerPageOptions={[5, 10, 25]}
            component="div"
            count={taxas.length}
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
            labelRowsPerPage="Linhas por página:"
            className="border-t border-gray-200"
          />
        )}
      </Paper>

      {/* Dialog */}
      <Dialog 
        open={openDialog} 
        onClose={handleCloseDialog} 
        maxWidth="md" 
        fullWidth
        PaperProps={{
          className: "rounded-lg"
        }}
      >
        <DialogTitle className="bg-gray-50 border-b border-gray-200">
          <Typography variant="h6" className="font-semibold">
            {editingTaxa ? 'Editar Taxa' : 'Nova Taxa'}
          </Typography>
        </DialogTitle>
        
        <form onSubmit={handleSubmit}>
          <DialogContent className="space-y-4 pt-4">
            <TextField
              fullWidth
              label="Nome da Taxa"
              value={formData.nome}
              onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
              required
              variant="outlined"
              className="mb-4"
            />
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <TextField
                fullWidth
                label="Valor"
                type="number"
                value={formData.valor}
                onChange={(e) => setFormData({ ...formData, valor: e.target.value })}
                inputProps={{ step: "0.01", min: "0" }}
                placeholder="0.00"
                variant="outlined"
              />
              
              <TextField
                fullWidth
                label="Percentagem (%)"
                type="number"
                value={formData.percentagem}
                onChange={(e) => setFormData({ ...formData, percentagem: e.target.value })}
                inputProps={{ step: "0.01", min: "0", max: "100" }}
                placeholder="0.00"
                variant="outlined"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <TextField
                fullWidth
                label="Valor Mínimo"
                type="number"
                value={formData.valor_minimo}
                onChange={(e) => setFormData({ ...formData, valor_minimo: e.target.value })}
                inputProps={{ step: "0.01", min: "0" }}
                placeholder="0.00"
                variant="outlined"
              />
              
              <TextField
                fullWidth
                label="Valor Máximo"
                type="number"
                value={formData.valor_maximo}
                onChange={(e) => setFormData({ ...formData, valor_maximo: e.target.value })}
                inputProps={{ step: "0.01", min: "0" }}
                placeholder="0.00"
                variant="outlined"
              />
            </div>
            
            <FormControl fullWidth variant="outlined">
              <InputLabel>Recorrência</InputLabel>
              <Select
                value={formData.recorencia}
                label="Recorrência"
                onChange={(e) => setFormData({ ...formData, recorencia: e.target.value })}
              >
                <MenuItem value=""><em>Selecione uma opção</em></MenuItem>
                {recorenciaOptions.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            
            <FormControlLabel
              control={
                <Switch
                  checked={formData.activo}
                  onChange={(e) => setFormData({ ...formData, activo: e.target.checked })}
                  color="primary"
                />
              }
              label="Taxa ativa"
              className="mt-2"
            />
          </DialogContent>
          
          <DialogActions className="bg-gray-50 border-t border-gray-200 px-6 py-4">
            <Button 
              onClick={handleCloseDialog}
              className="text-gray-600 hover:bg-gray-100"
            >
              Cancelar
            </Button>
            <Button 
              type="submit" 
              variant="contained"
              className="bg-blue-600 hover:bg-blue-700"
            >
              {editingTaxa ? 'Atualizar' : 'Criar'}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Box>
  );
};

export default TaxasPage;