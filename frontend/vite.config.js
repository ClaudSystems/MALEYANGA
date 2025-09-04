import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  // ⭐ REMOVA a linha root: './src' - o Vite já procura em src por padrão
  build: {
    outDir: '../backend/static/dist',  // Build vai para Django
    emptyOutDir: true,
  },
  server: {
    port: 3000,
    cors: true,
    host: true
  }
})