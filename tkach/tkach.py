import os

from flask import Flask, render_template, redirect, url_for

from forms import ArrayForm

from calculate import calculate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '\x15"\xf9\x90OpR\xc5o;!\x12L\xbf\xe0*\
                            \xb5\xf4\xcfR\xe7\xc1\xc8\xb5'
solution = []
MEDIA_FOLDER = "/Users/doorknob/dev/pythonVirtualEnvs/projects/tkach/tkach/static/graphs/"


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', solution=solution)


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = ArrayForm()
    if form.validate_on_submit():
        del solution[:]
        array = form.array.data
        for element in calculate(array):
            solution.append(element)
        return redirect(url_for('index'))
    return render_template('add.html', form=form)


@app.route('/uploads/graphs/')
def download_file(filename):
    return send_from_directory(MEDIA_FOLDER, filename, as_attachment=True)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
