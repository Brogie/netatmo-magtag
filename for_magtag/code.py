import board
import displayio
import neopixel
import time
import alarm
from getData import connect, extract_dashboard_data, get_access_token, get_graph_data_for_module, get_station_data
from graphs import draw_line_graph
from dashboards import draw_all_overviews, draw_current_min_max, show_text
from menu import open_menu
from station import station

def set_alarm(seconds):
    buttons = (board.BUTTON_A, board.BUTTON_D)
    pin_alarms = [
            alarm.pin.PinAlarm(
            pin=pin, 
            value=False, 
            pull=True
        ) for pin in buttons
    ]
    time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + seconds)
    alarm.exit_and_deep_sleep_until_alarms(time_alarm, *pin_alarms)

display = board.DISPLAY
screen = displayio.Group()

# wait until we can draw
# time.sleep(display.time_to_refresh)

module = alarm.sleep_memory[0]
sensor = alarm.sleep_memory[1]

try:
    if alarm.wake_alarm != None and (alarm.wake_alarm != None and alarm.wake_alarm.pin == board.BUTTON_D):
        pixels = neopixel.NeoPixel(board.NEOPIXEL, 4)
        pixels[0] = (255, 255, 255)
        pixels[1] = (255, 255, 255)
        pixels[2] = (255, 255, 255)
        pixels[3] = (255, 255, 255)

    if alarm.wake_alarm == None or (alarm.wake_alarm.pin != None and alarm.wake_alarm.pin == board.BUTTON_A):
        module, sensor = open_menu(
            display, alarm.sleep_memory[0], alarm.sleep_memory[1])
        alarm.sleep_memory[0] = module
        alarm.sleep_memory[1] = sensor
        show_text("Loading...")
except:
    pass

try:
    print('Connecting to wifi')
    requests = connect()
    print('Getting access token')
    access_token = get_access_token(requests)
    print('Getting station data')
    stationData = get_station_data(access_token, requests)
except:
    show_text("Connection Error")
    set_alarm(1200)

dst = 1
local_time = time.localtime(stationData['time_server'])
clock_text = str(local_time[3] + dst) + ':' + f"{local_time[4]:02d}"

print('Generating screen')
color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xBBBBBB
bg_sprite = displayio.TileGrid(
    color_bitmap, x=0, y=0, pixel_shader=color_palette)
screen.append(bg_sprite)

if station[module]['id'] != None:
    print('Getting graph data')
    graph_data, graph_min, graph_max = get_graph_data_for_module(
        station[module]['id'],
        station[module]['sensors'][sensor],
        stationData['time_server'],
        access_token,
        requests
    )

    print('Generating Graph')
    print(graph_data)
    screen = draw_line_graph(
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
    )

    print('Generating summary')
    suffix = ''
    if station[module]['sensors'][sensor] == 'temperature':
        suffix = 'c'
    elif station[module]['sensors'][sensor] == 'humidity':
        suffix = '%'
        
    screen = draw_current_min_max(
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
    )
else:
    modules = []
    dashboards = extract_dashboard_data(stationData)
    for i in range(len(station[module]['group_names'][sensor])):
        dashboard = dashboards[station[module]['group_ids'][sensor][i]]
        co2Value = 'n/a'
        if 'CO2' in dashboard:
            co2Value = dashboard['CO2']
        modules.append(
            {
                'name': station[module]['group_names'][sensor][i],
                'temp': dashboard['Temperature'],
                'humidity': dashboard['Humidity'],
                'co2': co2Value
            }
        )
    
    screen = draw_all_overviews(screen, modules, (int)(display.width))


print('Displaying screen')
display.show(screen)
display.refresh()

print('Done')

print('Setting alarm')
seconds_to_next_hour = 3600 - stationData['time_server'] % 3600
set_alarm(seconds_to_next_hour + 60)
