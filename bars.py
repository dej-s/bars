import json
from yandex_geocoder import Client
from geopy import distance

def coords_swap(coords):
    coords[1], coords[0] = coords[0], coords[1]
    return coords

def get_bar_distance(bar):
    return bar['distance']

def main():

    location = input("Где вы находитесь? ")

    mycoords = coords_swap(list(Client.coordinates(location)))



    #red_square_coords = coords_swap(list(Client.coordinates('Красная Площадь')))
    #vv_coords = coords_swap(list(Client.coordinates('Владивосток')))

    #print(red_square_coords)
    #print(vv_coords)

    #print(distance.distance(red_square_coords,vv_coords).km)

    #print('Ваши координаты: {}'.format(coords))


    bardata = []

    with open('data/data-2897-2019-04-09.json', encoding='cp1251') as jsonfile:
        bars_data = json.load(jsonfile)

    for bar in bars_data:
        title = bar['Name']
        latitude = bar['Latitude_WGS84']
        longitude = bar['Longitude_WGS84']

        bar_distance = distance.distance(mycoords, (latitude,longitude)).km
        bardata.append({'title':title, 'latitude':latitude, 'longitude':longitude, 'distance':bar_distance})


    print(min(bardata, key=get_bar_distance))

if __name__ == "__main__":
    main()
