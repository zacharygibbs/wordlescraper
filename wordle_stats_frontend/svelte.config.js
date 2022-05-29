import adapter from '@sveltejs/adapter-static';
/** @type {import('@sveltejs/kit').Config} */
import sveltePreprocess from "svelte-preprocess"
const config = {
	preprocess: sveltePreprocess(),
	kit: {
		// hydrate the <div id="svelte"> element in src/app.html
		adapter: adapter(),
		appDir: 'wordle-stats-sciencey/_app',
		prerender: {default: true},
		vite: {
			ssr: {
			  noExternal: ['@popperjs/core']
			}
		},
	}
};
export default config;
