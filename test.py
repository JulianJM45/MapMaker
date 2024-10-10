import requests
import math
from PIL import Image

ECF = 40075016.686   # Earth's circumference around the equator
POL_CF = 40007863    # Earth's circumference around poles



ZOOM = 14

coordinates = {'Northwest': [47.522879190486115, 11.001931378592806], 'SouthEast': [47.47766307884326, 11.09766845966403]}
icon_path = 'icons/120px-Firepit.png'
image_path = 'MyMaps/MyMap1.png'





def draw_firepits():
    nwLat, nwLon = coordinates['Northwest']
    seLat, seLon = coordinates['SouthEast']

    latitude = math.radians((nwLat + seLat) / 2)
    s_pixel = ECF * math.cos(latitude) / 2.0 ** (ZOOM + 8.0)

    # positions = []
    # for firepit in get_firepits(nwLat, nwLon, seLat, seLon):
    #     x_meters, y_meters = getMetersFromCoordinates(nwLat, firepit[0], firepit[1], nwLon)
    #     x, y = int(x_meters / s_pixel), int(y_meters / s_pixel)
    #     positions.append((x, y))

    print(get_firepits(nwLat, nwLon, seLat, seLon))
    positions = [(210, 750), (739, 448), (449, 363)]

    # print(positions)

    image = Image.open(image_path)
    icon = Image.open(icon_path)
    icon = icon.resize((20, 20))

    iamge = overlay_image(image, icon, positions)
    image.show()
    image.close()
    icon.close()


def overlay_image(image, icon, positions):
    for position in positions:
        image.paste(icon, position, icon)
    return image
    # Save the result

def get_firepits(nwLat, nwLon, seLat, seLon):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (
        node["leisure"="firepit"]({seLat},{nwLon},{nwLat},{seLon});
    );
    out center;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()

    firepits = []
    for element in data['elements']:
            if 'lat' in element and 'lon' in element:
                    firepits.append((element['lat'], element['lon']))
            elif 'center' in element:
                    firepits.append((element['center']['lat'], element['center']['lon']))

    return(firepits)

def getMetersFromCoordinates(north, south, east, west):
    widthMeters = (east - west) * (ECF * math.cos(math.radians((north+south)/2))) / 360
    heightMeters = (north - south) * POL_CF / 360
    return [widthMeters, heightMeters]

if __name__ == '__main__':
    draw_firepits()
