import math
import requests
import os
from PIL import Image, ImageDraw, ImageFont

POL_CF = 40007863    # Earth's circumference around poles
ECF = 40075016.686   # Earth's circumference around the equator



# icon_path = 'icons/120px-Firepit.png'


# myfont = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf" 
if os.name == 'nt':  # Windows
    myfont = "C:\\Windows\\Fonts\\Arial.ttf"
else:  # Linux and other UNIX-like systems
    myfont = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"



def getMap(index, coordinates, MAP_STYLE, ZOOM):
    nwLat, nwLon = coordinates['Northwest']
    seLat, seLon = coordinates['SouthEast']
    

    WIDTH_METERS, HEIGHT_METERS = getMetersFromCoordinates(nwLat, seLat, seLon, nwLon)
    # Calculate tiles 
    x1, y1 = deg2num(nwLat, nwLon, ZOOM)
    x2, y2 = deg2num(seLat, seLon, ZOOM)
    # Calculate Tile Corners Coordinates
    lat1, lon1 = num2deg(x1, y1, ZOOM)  
    # Calculate Pixels per Meter
    latitude = math.radians((nwLat + seLat) / 2)
    s_pixel = ECF * math.cos(latitude) / 2.0 ** (ZOOM + 8.0)
    # Calculate Pixel Dimensions
    pix_w = int(WIDTH_METERS / s_pixel)
    pix_h = int(HEIGHT_METERS / s_pixel)
    
    # Download Tiles
    print(f"Downloading Map {index+1} ...")
    download_tiles(x1, x2, y1, y2, ZOOM, MAP_STYLE)
    print("Tiles Downloaded")
    #create output Image
    output_image = stitchTiles(x1, x2, y1, y2, ZOOM)
    #crop Image
    map_image = cropBorders(nwLat, nwLon, lon1, lat1, s_pixel, pix_w, pix_h, output_image)
    map_image=label(map_image, s_pixel, index)
    map_image = draw_firepits(map_image, coordinates, s_pixel)
    # map_image.show()
    map_image.save(f'MyMaps/MyMap{index + 1}.png')





def getMetersFromCoordinates(north, south, east, west):
    widthMeters = (east - west) * (ECF * math.cos(math.radians((north+south)/2))) / 360
    heightMeters = (north - south) * POL_CF / 360
    return [widthMeters, heightMeters]


def getZoom(max_distance):
    return int(math.log((1.3*(POL_CF+ECF)/max_distance*2),2))


def heightFromCoordinates(north, south):
    return POL_CF*(north-south)/360


def widthFromCoordinates(west, east, latitude):
    return ECF*math.cos(math.radians(latitude))*(east-west)/360


def label(image, s_pixel, index):
    pix1 = int(1000/s_pixel)
    width, height = image.size
    ImageDraw.ImageDraw.font = ImageFont.truetype(myfont, 30)
    draw = ImageDraw.Draw(image)
    draw.text((width-10, height-10), f"Map {index+1}", fill=(255, 0, 0), anchor='rs', stroke_width=0)
    draw.line((10, height-10, 10+pix1, height-10), fill=(0, 0, 0), width=2)
    draw.line((10, height-15, 10, height-5), fill=(0, 0, 0), width=2)
    draw.line((10+pix1, height-15, 10+pix1, height-5), fill=(0, 0, 0), width=2)
    draw.text((10+(pix1/2), height-12), "1 km", fill=(0, 0, 0), anchor='ms', stroke_width=0)
    return image           


def stitchTiles(x1, x2, y1, y2, ZOOM):
    # Initialize List for Tile Images
    tile_images = []

    # Stitch Tiles Together
    for y in range(y1, y2 + 1):
        row_images = []
        for x in range(x1, x2 + 1):
            tile_filename = f"tiles/{ZOOM}_{x}_{y}.png"
            tile_image = Image.open(tile_filename)
            row_images.append(tile_image)
        tile_images.append(row_images)

    # Create a single image from tile_images
    image_width = sum(img.width for img in tile_images[0])
    image_height = sum(row[0].height for row in tile_images)
    output_image = Image.new("RGBA", (image_width, image_height))

    y_offset = 0
    for row_images in tile_images:
        x_offset = 0
        for tile_image in row_images:
            output_image.paste(tile_image, (x_offset, y_offset))
            x_offset += tile_image.width
        y_offset += row_images[0].height
    
    return output_image
    

def cropBorders(northwest_latitude, northwest_longitude, lon1, lat1, s_pixel, pix_w, pix_h, output_image):
    left_crop = int((ECF * math.cos(math.radians(northwest_latitude)) * abs(lon1 - northwest_longitude) / 360) / s_pixel)
    top_crop = int((POL_CF * abs(lat1 - northwest_latitude) / 360) / s_pixel)
    right_crop = left_crop + pix_w
    bottom_crop = top_crop + pix_h
    cropped_image = output_image.crop((left_crop, top_crop, right_crop, bottom_crop))
    return cropped_image


def download_tiles(x1, x2, y1, y2, ZOOM, MAP_STYLE):
    # Create Directory for Tiles
    if not os.path.exists("tiles"):
        os.makedirs("tiles")

    # Loop Through Tiles and Download
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            tile_url = f"https://{MAP_STYLE}/{ZOOM}/{x}/{y}.png"
            tile_filename = f"tiles/{ZOOM}_{x}_{y}.png"
            if not os.path.exists(tile_filename):
                #print(f"Getting {x},{y}")
                response = requests.get(tile_url)
                if response.status_code == 200:
                    with open(tile_filename, 'wb') as f:
                        f.write(response.content)


# Calculate Tile Coordinates
def deg2num(lat_deg, lon_deg, ZOOM):
    xtile = int((lon_deg + 180.0) / 360.0 * 2.0 ** ZOOM)
    lat_rad = math.radians(lat_deg)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi) * 2.0 ** (ZOOM - 1.0))
    return xtile, ytile


# Calculate Tile Corners Coordinates
def num2deg(x, y, ZOOM):
    lon = (x / 2**ZOOM)*360-180
    lat = math.atan(math.sinh(math.pi-(y/2**ZOOM)*2*math.pi))*180/math.pi
    return lat, lon


def draw_firepits(image, coordinates, s_pixel):
    nwLat, nwLon = coordinates['Northwest']
    seLat, seLon = coordinates['SouthEast']

    positions = []
    for firepit in get_firepits(nwLat, nwLon, seLat, seLon):
        # x_meters, y_meters = getMetersFromCoordinates(nwLat, firepit[0], firepit[1], nwLon)
        # x, y = int(x_meters / s_pixel), int(y_meters / s_pixel)
        x,y = get_xy(firepit[0], firepit[1], coordinates, image.width, image.height)
        positions.append((x, y))

    current_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(current_dir)
    icon_path = os.path.join(parent_dir, 'icons/120px-Firepit.png')

    icon = Image.open(icon_path)
    icon = icon.resize((20, 20))

    iamge = overlay_image(image, icon, positions)
    icon.close()
    return image


def overlay_image(image, icon, positions):
    for position in positions:
        image.paste(icon, position, icon)
    return image


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

def get_xy(lat, lon, coordinates, pix_w, pix_h):
    nwLat, nwLon = coordinates['Northwest']
    seLat, seLon = coordinates['SouthEast']

    x= int((lon - nwLon) / (seLon - nwLon) * pix_w)
    y= int((lat - nwLat) / (seLat - nwLat) * pix_h)

    return x, y