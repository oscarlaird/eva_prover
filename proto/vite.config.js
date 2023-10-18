import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit({
		onwarn: (warning, handler) => {
			if (warning.code === 'a11y-missing-attribute') return;
			handler(warning);
		}
	})],
});
