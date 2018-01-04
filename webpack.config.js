"use strict";
const path = require("path");
const webpack = require("webpack");
const ExtractTextPlugin = require("extract-text-webpack-plugin");
const ManifestRevisionPlugin = require("manifest-revision-webpack-plugin");
const rootAssetPath = path.join(__dirname, "src", "lerg_files_upload", "static");

(function (extractCss, webpack2) {
    module.exports = (env) => {
        const isDevBuild = !(env && env.prod);
        return {
            entry: {
                main: [
                    path.join(rootAssetPath, "css", "style.css")
                ],
                vendor: [
                    "jquery",
                    "bootstrap",
                    "bootstrap/dist/css/bootstrap.css",
                    "font-awesome/css/font-awesome.min.css",
                    path.join(rootAssetPath, "js", "upload.js")
                ]
            },
            output: {
                path: path.join(rootAssetPath, "dist"),
                publicPath: "/static/",
                filename: "[name].[hash].js",
                library: "[name]_[hash]"
            },
            resolve: {extensions: [".js", ".css"]},
            module: {
                rules: [
                    {
                        test: /\.css(\?|$)/,
                        use: extractCss.extract({
                            use: [
                                isDevBuild ? "css-loader" : "css-loader?minimize", "postcss-loader"
                            ]
                        })
                    },
                    {test: /\.(png|woff|woff2|eot|ttf|svg)(\?|$)/, use: "url-loader?limit=100000"}
                ]
            },
            stats: {modules: false},
            plugins: [
                new webpack2.ProvidePlugin({
                    $: "jquery",
                    jQuery: "jquery"
                }), // Maps these identifiers to the jQuery package (because Bootstrap expects it to be a global variable)
                extractCss,
                new ManifestRevisionPlugin(path.join(rootAssetPath, "dist", "manifest.json"), {
                    rootAssetPath: path.join(rootAssetPath, "static"),
                    ignorePaths: [rootAssetPath]
                })
            ].concat(isDevBuild ? [] : [new webpack2.optimize.UglifyJsPlugin()])
        };
    };
}(new ExtractTextPlugin("[name].[chunkhash].css"), webpack));
