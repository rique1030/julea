const path = require("path");

module.exports = {
  webpack: {
    alias: {
      "@components": path.resolve(__dirname, "src/components"),
      "@pages": path.resolve(__dirname, "src/pages"),
      "@assets": path.resolve(__dirname, "src/assets"),
      "@src": path.resolve(__dirname, "src"),
    },
    configure: (webpackConfig) => {
      webpackConfig.module.rules.push({
        test: /\.(woff|woff2|eot|ttf|otf)$/,
        type: "asset/resource",
      });
      webpackConfig.output.publicPath = "./";
      return webpackConfig;
    },
  },
};
