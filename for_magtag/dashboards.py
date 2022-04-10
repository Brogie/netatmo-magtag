from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from getData import get_graph_data_for_module
from station import station
from graphs import draw_line_graph
import terminalio
import displayio
import board

def show_text(text):
    display = board.DISPLAY
    screen = displayio.Group()
    color_bitmap = displayio.Bitmap(display.width, display.height, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x000000
    bg_sprite = displayio.TileGrid(
        color_bitmap, x=0, y=0, pixel_shader=color_palette)
    screen.append(bg_sprite)


    selected_module_text = label.Label(
        terminalio.FONT,
        text=text,
        color=0xFFFFFF,
        scale=3
    )
    selected_module_text.x = int(
        (display.width - (len(text) * 18)) / 2)
    selected_module_text.y = 50

    screen.append(selected_module_text)

    display.show(screen)
    display.refresh()

def draw_graph_screen(module, sensor, graph_data, graph_min, graph_max, clock_text, screen):
    print('Generating Graph')
    screen.append(draw_line_graph(
        station[module]['name'] + ' ' + station[module]['sensors'][sensor],
        graph_data,
        graph_min,
        graph_max,
        screen,
        5,
        5,
        210,
        119,
        True
    ))

    print('Generating summary')
    suffix = ''
    if station[module]['sensors'][sensor] == 'temperature':
        suffix = 'c'
    elif station[module]['sensors'][sensor] == 'humidity':
        suffix = '%'

    screen.append(draw_current_min_max(
        header_text=clock_text,
        current_value=graph_data[len(graph_data)-1],
        max_value=graph_max,
        min_value=graph_min,
        suffix=suffix,
        screen=screen,
        x=220,
        y=5,
        width=71,
        height=119
    ))

    return screen

def draw_current_min_max(header_text, current_value, max_value, min_value, suffix, screen, x=0, y=0, width=296, height = 128):
    shadow = RoundRect(x=x+2,y=y+2,width=width,height=height,r=10,fill=0x000000, outline=0x000000, stroke=2)
    screen.append(shadow)
    border = RoundRect(x=x,y=y,width=width,height=height,r=10,fill=0xFFFFFF, outline=0x000000, stroke=1)
    screen.append(border)

    header = RoundRect(x=x,y=y,width=width,height=20,r=10,fill=0x000000)
    headerBottom = Rect(x=x,y=y+10,width=width,height=10,fill=0x000000)
    screen.append(header)
    screen.append(headerBottom)

    text_area = label.Label(
        terminalio.FONT,
        text = header_text,
        color=0xFFFFFF,
    )
    text_area.x = x + int((width - (len(header_text) * 6)) / 2)
    text_area.y = 14

    screen.append(text_area)

    current_text = str(current_value) + suffix
    text_current = label.Label(
        terminalio.FONT,
        text = current_text,
        color=0x000000,
        scale=2
    )
    text_current.x = x + int((width - (len(current_text) * 12)) / 2)
    text_current.y = 45

    screen.append(text_current)

    max_text = 'max:' + str(max_value) + suffix
    label_max = label.Label(
        terminalio.FONT,
        text = max_text,
        color=0x000000,
    )
    label_max.x = x + int((width - (len(max_text) * 6)) / 2)
    label_max.y = 80

    screen.append(label_max)

    min_text = 'min:' + str(min_value) + suffix
    label_min = label.Label(
        terminalio.FONT,
        text = min_text,
        color=0x000000,
    )
    label_min.x = x + int((width - (len(min_text) * 6)) / 2)
    label_min.y = 100

    screen.append(label_min)

    return screen

def draw_all_overviews(screen, modules, screenWidth):
    x = 5
    width = ((screenWidth - 5) / len(modules)) - 5
    for i in range(len(modules)):
        draw_overview(screen, modules[i]['temp'], modules[i]['co2'], modules[i]['humidity'], modules[i]['name'], (int)(x + ((width + x) * i)), 5, (int)(width), 115)
    return screen

def draw_overview(screen, temp, co2, humidity, sensorName, x, y, width, height):
    shadow = RoundRect(x=x+2,y=y+2,width=width,height=height,r=10,fill=0x000000, outline=0x000000, stroke=2)
    screen.append(shadow)
    border = RoundRect(x=x,y=y,width=width,height=height,r=10,fill=0xFFFFFF, outline=0x000000, stroke=1)
    screen.append(border)

    header = RoundRect(x=x,y=y,width=width,height=20,r=10,fill=0x000000)
    headerBottom = Rect(x=x,y=y+10,width=width,height=10,fill=0x000000)
    screen.append(header)
    screen.append(headerBottom)

    text_area = label.Label(
        terminalio.FONT,
        text = sensorName,
        color=0xFFFFFF,
    )
    text_area.x = x + int((width - (len(sensorName) * 6)) / 2)
    text_area.y = 14

    screen.append(text_area)

    # Temp
    temp_h = 'Temp'
    header_temp = label.Label(
        terminalio.FONT,
        text = temp_h,
        color=0x000000,
        scale=1
    )
    header_temp.x = x + int((width - (len(temp_h) * 6)) / 2)
    header_temp.y = 30
    screen.append(header_temp)

    temp = str(temp) + 'c'
    label_temp = label.Label(
        terminalio.FONT,
        text = temp,
        color=0x000000,
        scale=2
    )
    label_temp.x = x + int((width - (len(temp) * 12)) / 2)
    label_temp.y = 45
    screen.append(label_temp)

    # Humidity
    hum_h = 'Humidity'
    header_hum = label.Label(
        terminalio.FONT,
        text = hum_h,
        color=0x000000,
        scale=1
    )
    header_hum.x = x + int((width - (len(hum_h) * 6)) / 2)
    header_hum.y = 60
    screen.append(header_hum)

    hum = str(humidity) + '%'
    label_hum = label.Label(
        terminalio.FONT,
        text = hum,
        color=0x000000,
        scale=2
    )
    label_hum.x = x + int((width - (len(hum) * 12)) / 2)
    label_hum.y = 75
    screen.append(label_hum)

    # CO2
    co2_h = 'co2'
    header_co2 = label.Label(
        terminalio.FONT,
        text = co2_h,
        color=0x000000,
        scale=1
    )
    header_co2.x = x + int((width - (len(co2_h) * 6)) / 2)
    header_co2.y = 90
    screen.append(header_co2)

    co2 = str(co2)
    label_co2 = label.Label(
        terminalio.FONT,
        text = co2,
        color=0x000000,
        scale=2
    )
    label_co2.x = x + int((width - (len(co2) * 12)) / 2)
    label_co2.y = 105

    screen.append(label_co2)