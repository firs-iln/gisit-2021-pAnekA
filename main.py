from flask import Flask
from jinja2 import Template
from os.path import join as path_to

app = Flask(__name__)


@app.route('/')
def index():
    with open(path_to('front', 'index.html'), encoding='utf-8') as html:
        with open(path_to('front', 'styles.css'), encoding='utf-8') as css:
            return Template(html.read()).render({'style': css.read()})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
