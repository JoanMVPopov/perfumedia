const { defineConfig } = require('@vue/cli-service')

const path = require('path');
const dotenv = require('dotenv');

// Load .env from project root
dotenv.config({
  path: path.resolve(__dirname, '../.env')
});

module.exports = defineConfig({
  configureWebpack: {
            entry: "./src/main.js",
            devServer: {
                hot: true,
                allowedHosts: [
                  'perfumedia.info',
                  // If you might use subdomains like app.perfumedia.info in the future,
                  // you can also add a wildcard for subdomains:
                  '.perfumedia.info',
                ],
            },
            watch: true,
            watchOptions: {
                ignored: /node_modules/,
                poll: 1000,
            },
        },
  transpileDependencies: true
})
