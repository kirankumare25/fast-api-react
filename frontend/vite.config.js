import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // Needed for the Docker Container port mapping to work
    port: 5173, // You can replace this port with any port
    watch: {
      usePolling: true // For file watching inside the container
    }
  },
});
