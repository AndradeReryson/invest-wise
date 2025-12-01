import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // Toda vez que o código chamar '/windmill-proxy', o Vite redireciona para o Windmill
      '/windmill-proxy': {
        target: 'https://app.windmill.dev',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/windmill-proxy/, '')
      }
    }
  }
})