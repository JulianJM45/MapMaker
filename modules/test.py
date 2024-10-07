import math
import os
from PIL import Image, ImageDraw, ImageFont
import mgrs

POL_CF = 40007863    # Earth's circumference around poles
ECF = 40075016.686   # Earth's circumference around the equator



def main():
    image = load_image()
    nwLat, nwLon, seLat, seLon, s_pixel = 49.375692048390896, 8.071310177849329, 49.33047593674804, 8.17060266394755, 6.223844132776964

    image = addMGRSGrid(image, nwLat, nwLon, seLat, seLon, s_pixel, MGRS=500)
    image.show()









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
            print(f'eastern: {eastern}')
            draw.line([((P1_easting + i) / s_pixel, 42-level*8), ((P2_easting + i) / s_pixel, pix_h-42+level*7)], fill=(255, 105, 180, 200), width=3)
            draw.text(((P1_easting + i) / s_pixel, 2), f'{eastern}', fill=(255, 105, 180, 200), anchor='mt', stroke_width=0, font=font)
            draw.text(((P2_easting + i) / s_pixel, pix_h-2), f'{eastern}', fill=(255, 105, 180, 200), anchor='mb', stroke_width=0, font=font)



        draw.text((2, 2), f'{nw_GZD} {nw_GSI}', fill=(255, 90, 140, 255), anchor='lt', stroke_width=0, font=ImageFont.truetype("arial.ttf", 18))
    
    return map_image


def getMetersFromCoordinates(north, south, east, west):
    widthMeters = (east - west) * (ECF * math.cos(math.radians((north+south)/2))) / 360
    heightMeters = (north - south) * POL_CF / 360
    return [widthMeters, heightMeters]



def load_image():
    image_path = os.path.join("MyMaps", "MyMap1.png")
    # print(f"Loading image from {image_path}")
    image = Image.open(image_path)
    return image




if __name__ == '__main__':
    main()  