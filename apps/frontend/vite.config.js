import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: true,
    allowedHosts: [
      'localhost',
      '127.0.0.1',
      'my-life-abroad.com',
      'www.my-life-abroad.com',
      '.my-life-abroad.com'
    ]
  },
})