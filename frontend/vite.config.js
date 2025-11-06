import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

<<<<<<< HEAD
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
=======
export default defineConfig({
  base: '/gaah-bookkeeping-render/', 
  plugins: [vue()]
>>>>>>> 1c071df926c702b72a64ef539685c19e319a01de
})
