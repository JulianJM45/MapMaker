import os
import subprocess
import platform
import re
import img2pdf

from .get_map import *
from app import send_message_to_js


def render_maps(coordinates_list, config):
    MAP_STYLE = config['tile_layer']
    WIDTH = config['width']
    HEIGHT = config['height']
    SCALE = config['scale']
    ZOOM = config['zoom']
    AutoZoom = config['autoZoom']
    upscale = config['upscale']
    Overview = config['overview']
    PDF = config['pdf']

    print("Sending coordinates to Python:", coordinates_list)
    print("Selected Tile Layer:", MAP_STYLE)
    if upscale: print("upscaling")
    else: print ("no upscaling")
    max_distance=max(WIDTH, HEIGHT)
    if AutoZoom: ZOOM = getZoom(max_distance *SCALE/1000)
    print (ZOOM)
    if not os.path.exists("MyMaps"):
            os.makedirs("MyMaps")
    odd_maps = []
    even_maps = []
    if Overview:
        send_message_to_js("Downloading Overview Map...") 
        overviewImage, ovmc = overviewMap(coordinates_list, MAP_STYLE, WIDTH, HEIGHT)
                
    for index, coordinates in enumerate(coordinates_list):
        send_message_to_js(f"Downloading Map {index + 1}...")
        getMap(index, coordinates, MAP_STYLE, ZOOM)
        # Extract and assign the coordinates to separate variables
        
        if index % 2 == 0:
            odd_maps.append(f'MyMaps/MyMap{index + 1}.png')
        else: even_maps.append(f'MyMaps/MyMap{index + 1}.png')
        if Overview: 
            overviewImage = drawMapInOverview(overviewImage, ovmc, coordinates, index)

    # Delete the "tiles" directory and its contents
    if os.path.exists("tiles"):
        import shutil
        shutil.rmtree("tiles")
    print('download finished :)')
    send_message_to_js("Download finished")

    # Upscale the images if applicable
    if upscale:
        send_message_to_js("Upscaling maps...")
        map_files = os.listdir('MyMaps')
        for map_file in map_files:
            if 'OverviewMap' in map_file: continue  # Skip this iteration              
            upscaling(map_file, send_message_to_js)      
        print('upscale finished :)')
        send_message_to_js("Upscale finished")

    image_paths = odd_maps + even_maps
    if Overview:
        overviewImage.save('MyMaps/OverviewMap.png')
        image_paths.append('MyMaps/OverviewMap.png')
    if PDF:
        PDFgen(image_paths)
        if os.path.exists("MyMaps"):
                shutil.rmtree("MyMaps")
    send_message_to_js("Process finished :)")





def drawMapInOverview(overviewImage, ovmc, coordinates, index):
    width, height = overviewImage.size
    transparent_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(transparent_layer)
    fill_color = (0, 100, 255, 30)  # Blue with 50% transparency (RGBA)
    outline_color = (24, 116, 205, 200)  # Blue without transparency (RGB)
    x1 = width*(abs(coordinates['Northwest'][1]-ovmc[1])/abs(ovmc[1]-ovmc[3]))
    y1 = height*(abs(coordinates['Northwest'][0]-ovmc[0])/abs(ovmc[0]-ovmc[2]))
    x2 = width*(abs(coordinates['SouthEast'][1]-ovmc[1])/abs(ovmc[1]-ovmc[3]))
    y2 = height*(abs(coordinates['SouthEast'][0]-ovmc[0])/abs(ovmc[0]-ovmc[2]))
    draw.rectangle([x1, y1, x2, y2], fill=fill_color)
    draw.rectangle([x1, y1, x2, y2], outline=outline_color, width=4)
    # Add a number in the middle of the rectangle
    number = str(index + 1)
    font = ImageFont.truetype(myfont, size=50)  # Adjust the path and size
    text_x = (x1 + x2) // 2
    text_y = (y1 + y2 ) // 2
    draw.text((text_x, text_y), number, fill=(0, 0, 255), anchor='mm', font=font, stroke_width=1)
    overviewImage.paste(transparent_layer, (0, 0), transparent_layer)
    return overviewImage



def overviewMap(coordinates_list, MAP_STYLE, WIDTH, HEIGHT):
    # Initialize variables to store the maximum values
    max_north = max_south = max_east = max_west = None
    # Iterate through the coordinates_list
    for coordinates in coordinates_list:
        northwest = coordinates['Northwest']
        southeast = coordinates['SouthEast']        
        if max_north is None or northwest[0] > max_north:
            max_north = northwest[0]       
        if max_south is None or southeast[0] < max_south:
            max_south = southeast[0]
        if max_east is None or southeast[1] > max_east:
            max_east = southeast[1]
        if max_west is None or northwest[1] < max_west:
            max_west = northwest[1]
    max_north = max_north + 0.01
    max_west = max_west - 0.01
    max_south = max_south - 0.01
    max_east = max_east + 0.01
    latitude = (max_north+max_south)/2
    longitude = (max_east+max_west)/2
    height = heightFromCoordinates(max_north, max_south)
    width = widthFromCoordinates(max_west, max_east, latitude)
    max_distance = max(height, width)
    ZOOM = getZoom(max_distance)
    #rescaling
    if width > (height*WIDTH/HEIGHT):
        height = width*HEIGHT/WIDTH
        max_north = latitude + 360*(height/2)/POL_CF
        max_south = latitude - 360*(height/2)/POL_CF
    elif height > (width*HEIGHT/WIDTH):
        width = height*WIDTH/HEIGHT
        max_east = longitude + 360*(width/2)/(ECF*math.cos(math.radians(latitude)))
        max_west = longitude - 360*(width/2)/(ECF*math.cos(math.radians(latitude)))
    # Calculate Pixel Dimensions
    s_pixel = ECF * math.cos(math.radians(latitude)) / 2.0 ** (ZOOM + 8.0)
    pix_w = int(width / s_pixel)
    pix_h = int(height / s_pixel)
    # Calculate tiles 
    x1, y1 = deg2num(max_north, max_west, ZOOM)
    x2, y2 = deg2num(max_south, max_east, ZOOM)
    # Calculate Tile Corners Coordinates
    lat1, lon1 = num2deg(x1, y1, ZOOM)  
    ovmc = [max_north, max_west, max_south, max_east]
    print("Downloading Overview Map ...")
    download_tiles(x1, x2, y1, y2, ZOOM, MAP_STYLE)
    #create output Image
    overviewImage = stitchTiles(x1, x2, y1, y2, ZOOM)
    overviewImage = cropBorders(max_north, max_west, lon1, lat1, s_pixel, pix_w, pix_h, overviewImage)
    return overviewImage, ovmc


def PDFgen(image_paths):
    # Create a PDF file to write the images into
    pdf_filename = 'MyRoute.pdf'
    # Check if the initial filename already exists
    file_exists = os.path.exists(pdf_filename)
    # If it exists, enumerate the filename
    if file_exists:
        base_name, extension = os.path.splitext(pdf_filename)
        count = 2
        while True:
            new_filename = f'{base_name}{count}{extension}'
            if not os.path.exists(new_filename):
                pdf_filename = new_filename
                break
            count += 1
    # Convert the images to PDF and save to the output file
    with open(pdf_filename, 'wb') as pdf_output:
        pdf_output.write(img2pdf.convert(image_paths))
    print(f'PDF created: {pdf_filename}')

    
def upscaling(map_file, print_message):
    map_file_without_extension, _ = os.path.splitext(map_file)

    current_dir = os.path.dirname(os.path.realpath(__file__))

    if platform.system() == 'Windows':
        executable = 'realesrgan-ncnn-vulkan.exe'
    elif platform.system() == 'Linux':
        executable = 'realesrgan-ncnn-vulkan'
    elif platform.system() == 'Darwin':
        executable = 'realesrgan-ncnn-vulkan'
    else:
        print('Unknown OS')
    # Define the command as a list of strings
    executablefile = os.path.join(current_dir, executable)

    command = [executablefile,'-i', f'MyMaps/{map_file}','-o', f'MyMaps/{map_file}', '-n', 'realesrgan-x4plus']
    # Run the command
    process = subprocess.Popen(command, stderr=subprocess.PIPE, text=True)
    for line in iter(process.stderr.readline, ''):
        print(line, end='')
        # Extract the number
        match = re.search(r'(\d+.\d+)%', line)
        if match:            
            number = float(match.group(1).replace(',', '.') )
            # print('Progress:', number)
            print_message(f'upscaling {map_file_without_extension}:\u2003{number}%')

