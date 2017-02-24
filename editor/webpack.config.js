var path = require("path");
var webpack = require("webpack");

module.exports = {
    entry: "./js/main.js",
    output: {
        path: path.resolve(__dirname, "build"),
        filename: "bundle.js"
    },
    module: {
        loaders: [
            {
                test: /\.js$/,
                loader: "babel-loader",
                query: {
                    presets: ["es2015"]
                }
            },
            {
                test: /\.scss$/,
                loaders: [ "style-loader", "css-loader", "sass-loader" ]
            }
        ]
    },
    stats: {
        colors: true
    },
    devtool: "source-map"
};
