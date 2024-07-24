// src input
// dest(destination) output
const { src, dest, watch, series } = require("gulp");
const sass = require("gulp-sass")(require("sass"));

function buildStyle() {
  return src("styles/scss/*.scss")
    .pipe(sass().on("error", sass.logError))
    .pipe(dest("styles/"));
}

// sync update
function watchTask() {
  watch("styles/scss/*.scss", buildStyle);
}

exports.default = series(buildStyle, watchTask);
