import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],

  logLevel: 'info',
  
  base: './',
  
  // 开发服务器配置
  server: {
    port: 5173,
    strictPort: true,
    host: '127.0.0.1',
    cors: true,
    headers: {
      'Access-Control-Allow-Origin': '*'
    }
  },
  
  build: {
    outDir: 'front_dist',
    assetsDir: 'assets',
    emptyOutDir: true,
    sourcemap: false
  },
  
  resolve: {
    alias: {
      '@': path.resolve(import.meta.dirname, './src')
    }
  }
})