const gulp = require("gulp");

const css = () => {
    const postCSS = require("gulp-postcss");
    const sass = require("gulp-sass");
    const minify = require("gulp-csso");
    sass.compiler = require("node-sass");
    return gulp
        // 파일 리소스 찾음
        .src("assets/scss/styles.scss")
        // css코드로 변환
        .pipe(sass().on("error", sass.logError))
        // tailwindcss, autoprefixer를 css로 변환
        .pipe(postCSS([require("tailwindcss"), require("autoprefixer")]))
        //  코드를 단순화
        .pipe(minify())
        // static/css 경로로 보냄
        .pipe(gulp.dest("static/css"));
};

exports.default = css;