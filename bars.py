# -*- coding: utf-8 -*
import json
from yandex_geocoder import Client
from geopy import distance
import folium
from flask import Flask


def coords_swap(coords):
    coords[1], coords[0] = coords[0], coords[1]
    return coords

def get_bar_distance(bar):
    return bar['distance']

def hello_world():
    with open('output/index.html', encoding='utf-8') as html_file:
        return html_file.read()


def main():

    location = input("Где вы находитесь? ")

    mycoords = coords_swap(list(Client.coordinates(location)))

    bardata = []

    with open('data/data-2897-2019-04-09.json', encoding='cp1251') as jsonfile:
        bars_data = json.load(jsonfile)

    for bar in bars_data:
        title = bar['Name']
        latitude = float(bar['Latitude_WGS84'])
        longitude = float(bar['Longitude_WGS84'])

        bar_distance = distance.distance(mycoords, (latitude,longitude)).km
        bardata.append({'title':title, 'latitude':latitude, 'longitude':longitude, 'distance':bar_distance})


    sorted_bars =  sorted(bardata, key=get_bar_distance)

    map = folium.Map(location=[float(mycoords[0]), float(mycoords[1])])
    tooltip = 'Бар здесь!'

    for item in sorted_bars[:5]:
        title = item['title']
        folium.Marker([item['latitude'], item['longitude']], popup='<b>{}</b>'.format(title), \
                      tooltip=tooltip).add_to(map)

    map.save('output/index.html')

    app = Flask(__name__)

    app.add_url_rule('/', 'hello', hello_world)
    app.run('0.0.0.0')

if __name__ == "__main__":
    main()
