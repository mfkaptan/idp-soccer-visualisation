var gulp = require('gulp');
var sass = require('gulp-sass');
var watch = require('gulp-watch');
var rename = require('gulp-rename');
var gzip = require('gulp-gzip');
var process = require('child_process');


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

gulp.task('default', ['django', 'sass', 'watch']);
