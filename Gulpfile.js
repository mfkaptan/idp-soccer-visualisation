var gulp = require('gulp');
var sass = require('gulp-sass');
var watch = require('gulp-watch');
var rename = require('gulp-rename');
var gzip = require('gulp-gzip');
var imagemin = require('gulp-imagemin');
var process = require('child_process');

var imageFolders = ['static', 'media'];

/* Compile Our Sass */
gulp.task('sass', function () {
    return gulp.src('apps/frontend/static/scss/*.scss')
        .pipe(sass({outputStyle: 'compressed'}))
        .pipe(gulp.dest('apps/frontend/static/css'));
});

/* Watch Files For Changes */
gulp.task('watch', function () {
    gulp.watch('apps/frontend/static/scss/**/*.scss', ['sass']);
});

/* Launch Django development server */
gulp.task('django', function () {
    process.spawn('./env/bin/python', ['-Wi', 'manage.py', 'runserver', '0.0.0.0:8000'], {
        detached: false,
        stdio: 'inherit'
    });
});

/* Optimizes images */
gulp.task('compress-images', function() {
    imageFolders.forEach(function(folder) {
        gulp.src(folder + '/**/*.{png,gif,jpeg,jpg}')
            .pipe(imagemin({progressive: true}))
            .pipe(gulp.dest('static/'));
    });
});

gulp.task('default', ['django', 'sass', 'watch']);
