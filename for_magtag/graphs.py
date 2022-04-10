import displayio
import terminalio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.sparkline import Sparkline

def draw_line_graph(header_text, graph_data, min, max, screen, x=0, y=0, width=296, height = 128, show_zero = False): 
    shadow = RoundRect(x=x+2,y=y+2,width=width,height=height,r=10,fill=0x000000, outline=0x000000, stroke=2)
    screen.append(shadow)
    border = RoundRect(x=x,y=y,width=width,height=height,r=10, fill=0xFFFFFF,outline=0x000000, stroke=1)
    screen.append(border)

    padding = 1
    if(max - min > 200): padding = 50

    if show_zero:
        zeroLine = Sparkline(
            width=width, height=height-20, max_items=48, y_min=min - padding, y_max= max + padding, x=x, y=y+20, color=0x888888
        )

        zeroLine.add_value(0)
        zeroLine.add_value(0)
        zeroLine.add_value(0)

        screen.append(zeroLine)

    dataLine = Sparkline(
        width=width, height=height-20, max_items=48, y_min=min - padding, y_max=max + padding, x=x, y=y+20, color=0x000000
    )

    for item in graph_data:
        dataLine.add_value(item)

    screen.append(dataLine)

    header = RoundRect(x=x,y=y,width=width,height=20,r=10,fill=0x000000)
    headerBottom = Rect(x=x,y=y+10,width=width,height=10,fill=0x000000)
    screen.append(header)
    screen.append(headerBottom)

    header_text = header_text
    text_area = label.Label(
        terminalio.FONT,
        text = header_text,
        color=0xFFFFFF,
    )
    text_area.x = 14
    text_area.y = 14

    screen.append(text_area)

    return screen