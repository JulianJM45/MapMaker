import math
import requests
import os
from PIL import Image, ImageDraw, ImageFont
import mgrs

POL_CF = 40007863    # Earth's circumference around poles
ECF = 40075016.686   # Earth's circumference around the equator

# myfont = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf" 
if os.name == 'nt':  # Windows
    myfont = "C:\\Windows\\Fonts\\Arial.ttf"
else:  # Linux and other UNIX-like systems
    myfont = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"



def getMap(index, coordinates, MAP_STYLE, ZOOM, MGRS):
    nwLat, nwLon = coordinates['Northwest']
    seLat, seLon = coordinates['SouthEast']

    # WIDTH_METERS, HEIGHT_METERS = getMetersFromCoordinates(nwLat, seLat, seLon, nwLon)
    # Calculate tiles 
    x1, y1 = deg2num(nwLat, nwLon, ZOOM)
    x2, y2 = deg2num(seLat, seLon, ZOOM)
    # Calculate Tile Corners Coordinates
    lat1, lon1 = num2deg(x1, y1, ZOOM)  
    # Calculate Pixels per Meter
    latitude = math.radians((nwLat + seLat) / 2)
    s_pixel = ECF * math.cos(latitude) / 2.0 ** (ZOOM + 8.0)
    # # Calculate Pixel Dimensions
    # pix_w = int(WIDTH_METERS / s_pixel)
    # pix_h = int(HEIGHT_METERS / s_pixel)
    
    # Download Tiles
    print(f"Downloading Map {index+1} ...")
    download_tiles(x1, x2, y1, y2, ZOOM, MAP_STYLE)
    print("Tiles Downloaded")
    #create output Image
    output_image = stitchTiles(x1, x2, y1, y2, ZOOM)
    #crop Image
    map_image = cropBorders(nwLat, nwLon, seLat, seLon, lon1, lat1, s_pixel, output_image)
    MGRS = 0
    if MGRS != 0: addMGRSGrid(map_image, nwLat, nwLon, seLat, seLon, s_pixel, MGRS)
    # print(map_image, nwLat, nwLon, seLat, seLon, s_pixel)
    map_image=label(map_image, s_pixel, index)
    map_image.show()
    map_image.save(f'MyMaps/MyMap{index + 1}.png')





def addMGRSGrid(map_image, nwLat, nwLon, seLat, seLon, s_pixel, MGRS=500):
    font=ImageFont.truetype("arial.ttf", 14)
    WIDTH_METERS, HEIGHT_METERS = getMetersFromCoordinates(nwLat, seLat, seLon, nwLon)
    level = len(str(MGRS)) - 1
    pix_w = int(WIDTH_METERS / s_pixel)
    pix_h = int(HEIGHT_METERS / s_pixel)

    m = mgrs.MGRS()
    draw = ImageDraw.Draw(map_image)

    NW = m.toMGRS(nwLat, nwLon, MGRSPrecision=5)
    nw_GZD, nw_GSI, nw_eastern, nw_northern = NW[:3], NW[3:5], NW[5:10], NW[10:]
    NE = m.toMGRS(nwLat, seLon, MGRSPrecision=5)
    ne_GZD, ne_GSI, ne_eastern, ne_northern = NE[:3], NE[3:5], NE[5:10], NE[10:]
    SE = m.toMGRS(seLat, seLon, MGRSPrecision=5)
    se_GZD, se_GSI, se_eastern, se_northenr = SE[:3], SE[3:5], SE[5:10], SE[10:]
    SW = m.toMGRS(seLat, nwLon, MGRSPrecision=5)
    sw_GZD, sw_GSI, sw_eastern, sw_northern = SW[:3], SW[3:5], SW[5:10], SW[10:]

    if nw_GZD==se_GZD and nw_GSI==se_GSI:
        base_northern = int(min(nw_northern, ne_northern)[:-level])* 10**level

        P1_northing = (int(nw_northern) - base_northern)
        P2_northing = (int(ne_northern) - base_northern)

        for i in range(0, int(HEIGHT_METERS), MGRS):
            northern = int((base_northern - i) / 10**level)
            draw.line([(42-level*8, (P1_northing + i) / s_pixel), (pix_w-42+level*7, (P2_northing + i) /s_pixel)], fill=(255, 105, 180, 200), width=3)
            draw.text((2, (P1_northing + i) / s_pixel), f'{northern}', fill=(255, 105, 180, 200), anchor='lm', stroke_width=0, font=font)
            draw.text((pix_w-2, (P2_northing + i) / s_pixel), f'{northern}', fill=(255, 105, 180, 200), anchor='rm', stroke_width=0, font=font)

        
        base_eastern = (int(min(nw_eastern, sw_eastern)[:-level])+1)* 10**level

        P1_easting = (base_eastern - int(nw_eastern))
        P2_easting = (base_eastern - int(sw_eastern))

        for i in range(0, int(WIDTH_METERS), MGRS): 
            eastern = int((base_eastern + i) / 10**level)
            draw.line([((P1_easting + i) / s_pixel, 42-level*8), ((P2_easting + i) / s_pixel, pix_h-42+level*7)], fill=(255, 105, 180, 200), width=3)
            draw.text(((P1_easting + i) / s_pixel, 2), f'{eastern}', fill=(255, 105, 180, 200), anchor='mt', stroke_width=0, font=font)
            draw.text(((P2_easting + i) / s_pixel, pix_h-2), f'{eastern}', fill=(255, 105, 180, 200), anchor='mb', stroke_width=0, font=font)



        draw.text((2, 2), f'{nw_GZD} {nw_GSI}', fill=(255, 90, 140, 255), anchor='lt', stroke_width=0, font=ImageFont.truetype("arial.ttf", 18))
    
    return map_image





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
    
# def cropBorders(northwest_latitude, northwest_longitude, lon1, lat1, s_pixel, pix_w, pix_h, output_image):
def cropBorders(nwLat, nwLon, seLat, seLon, lon1, lat1, s_pixel, output_image):
    WIDTH_METERS, HEIGHT_METERS = getMetersFromCoordinates(nwLat, seLat, seLon, nwLon)
    # Calculate Pixel Dimensions
    pix_w = int(WIDTH_METERS / s_pixel)
    pix_h = int(HEIGHT_METERS / s_pixel)

    left_crop = int((ECF * math.cos(math.radians(nwLat)) * abs(lon1 - nwLon) / 360) / s_pixel)
    top_crop = int((POL_CF * abs(lat1 - nwLat) / 360) / s_pixel)
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

