const CracoAlias = require("craco-alias");

module.exports = {
  plugins: [
    {
      plugin: CracoAlias,
      options: {
        source: "tsconfig",
        baseUrl: "./src",
        tsConfigPath: "./tsconfig.extend.json",
      },
    },
  ],
  webpack: {
    configure: (webpackConfig, { env, paths }) => {
      // Adds the crypto polyfill only in development - helped solve some persistent errors
      if (env === "development") {
        webpackConfig.resolve = {
          ...webpackConfig.resolve,
          fallback: {
            ...webpackConfig.resolve.fallback,
            crypto: require.resolve("crypto-browserify"),
          },
        };
      }

      return webpackConfig;
    },
  },
};
