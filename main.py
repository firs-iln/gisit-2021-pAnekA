from flask import Flask
from jinja2 import Template
from os.path import join as path_to
from pyproj import Proj, transform
from pyproj import Transformer
import json

app = Flask(__name__)


def convert_elem(elem: list):
    elem = list(convert(elem[0], elem[1]))
    return elem


def parse(geojson):
    geojson = geojson['features']
    res = [{
        "type": "Feature",
        "properties": {
            "info": "Path 9"
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [[]
            ]
        }
    }]
    print(type(geojson), type(res))
    for elem in geojson:
        elem = elem['properties']
        if elem == geojson[0]:
            elem1 = list(map(float, elem['start'].split(', ')))
            elem2 = list(map(float, elem['end'].split(', ')))
            elem1, elem2 = convert_elem(elem1), convert_elem(elem2)
            res[0]['geometry']['coordinates'][0].append(elem1)
            res[0]['geometry']['coordinates'][0].append(elem2)
        else:
            elem = list(map(float, elem['end'].split(', ')))
            elem = convert_elem(elem)
            res[0]['geometry']['coordinates'][0].append(elem)
    return json.dumps(res)


def convert(long: float, lat: float):
    x2, y2 = Transformer.from_crs('epsg:32652', 'epsg:4326').transform(long, lat)
    return x2, y2


@app.route('/')
def index():
    with open(path_to('front', 'index.html'), encoding='utf-8') as html:
        with open(path_to('front', 'styles.css'), encoding='utf-8') as css:
            return Template(html.read()).render({'style': css.read()})


@app.route('/path/<path>')
def send_path(path: int):
    with open(path_to('front', f'path_{path}.geojson'), encoding='utf-8') as file:
        file = file.read()
        print(type(file))
        file = json.loads(file)
        file = parse(file)
        print(file)
        return file


if __name__ == '__main__':
    print(1, convert(508021.130256, 6816885.36582), convert(508471.998019, 6817029.18292))
    app.run(host='127.0.0.1', port=8080)
