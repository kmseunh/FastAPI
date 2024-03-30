import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import ts from 'vite-plugin-ts';

export default defineConfig({
    plugins: [sveltekit(), ts()],
    server: {
        proxy: {
            '/api': {
                target: 'http://127.0.0.1:8000',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api/, ''),
            },
        },
    },
});
