import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    open: true,
    proxy: {
      '/transactions': {
        target: 'http://localhost:8000', // backend API URL
        changeOrigin: true
      },
      '/books': {
        target: 'http://localhost:8000', // backend API URL
        changeOrigin: true
      }
    }
  }
})
