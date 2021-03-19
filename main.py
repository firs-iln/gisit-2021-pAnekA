from flask import Flask, request
from jinja2 import Template
from os.path import join as path_to

app = Flask(__name__)


@app.route('/')
def index():
    with open(path_to('front', 'index.html'), encoding='utf-8') as html:
        with open(path_to('front', 'styles.css'), encoding='utf-8') as css:
            return Template(html.read()).render({'style': css.read()})


@app.route('/path/<path>')
def send_path(path):
    with open(path_to('front', f'path_{path}.geojson'), encoding='utf-8') as file:
        return file.read()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
