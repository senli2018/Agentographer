import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue';
import { resolve } from "path"

import AutoImport from 'unplugin-auto-import/vite';
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver, AntDesignVueResolver } from 'unplugin-vue-components/resolvers'

export default defineConfig({
	plugins: [
		vue(),

		AutoImport({
			resolvers: [ElementPlusResolver(), AntDesignVueResolver()],
			imports: ['vue', 'vue-router']
		}),
		Components({
			resolvers: [ElementPlusResolver(), AntDesignVueResolver({
				resolveIcons: true,
				importStyle: 'less'
			})],
		}),
	],
	css: {
		preprocessorOptions: {
			less: {
				javascriptEnabled: true,
				modifyVars: {
					'primary-color': '#1890ff',
				},
			},
		},
	},
	resolve: {

		alias: {
			'@': resolve(__dirname, './src'),
		},
	},

	server:{
		host: '0.0.0.0',
		port: 5173,
		proxy:{
			'/api': {
				target: 'http://localhost:8000',
				changeOrigin: true,
				secure: false,
				rewrite: (path) => path.replace(/^\/api/, '/api')
			}
		}
	}
});
