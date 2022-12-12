module.exports = {
  lintOnSave: false,
  runtimeCompiler: true,
  configureWebpack: {
    //Necessary to run npm link https://webpack.js.org/configuration/resolve/#resolve-symlinks
    resolve: {
       symlinks: false
    }
  },
  publicPath: '/',
  outputDir: 'dist',
  assetsDir: 'static',
  // css: {
  //   loaderOptions: {
  //     scss: {
  //       prependData: `
  //         @import "@/styles/variables.scss";
  //       `
  //     }
  //   }
  // },
  devServer: {
    proxy: {
      '^/api': {
        target: `http://localhost:5001`,
        changeOrigin: true
      }
    }
  },
  transpileDependencies: [
    '@coreui/utils',
    '@coreui/vue'
  ]
}
