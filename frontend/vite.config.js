import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: '../static/react-build',
    emptyOutDir: true,
    rollupOptions: {
      output: {
        manualChunks: undefined,
      },
    },
  },
  server: {
    proxy: {
      '/analyze': 'http://localhost:5001',
      '/results': 'http://localhost:5001',
      '/ratio': 'http://localhost:5001',
      '/static': 'http://localhost:5001',
    }
  }
})
