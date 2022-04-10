import displayio
import keypad
from station import station
from adafruit_display_text import label
import terminalio
import board
import time


def open_menu(display, module, sensor):
    selected = False

    while selected == False:
        screen = displayio.Group()
        color_bitmap = displayio.Bitmap(display.width, display.height, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0x000000
        bg_sprite = displayio.TileGrid(
            color_bitmap, x=0, y=0, pixel_shader=color_palette)
        screen.append(bg_sprite)

        selected_module_name = station[module]['name']
        selected_sensor_name = station[module]['sensors'][sensor]

        selected_module_text = label.Label(
            terminalio.FONT,
            text=selected_module_name,
            color=0xFFFFFF,
            scale=3
        )
        selected_module_text.x = int(
            (display.width - (len(selected_module_name) * 18)) / 2)
        selected_module_text.y = 25

        screen.append(selected_module_text)

        selected_sensor_text = label.Label(
            terminalio.FONT,
            text=selected_sensor_name,
            color=0xFFFFFF,
            scale=3
        )
        selected_sensor_text.x = int(
            (display.width - (len(selected_sensor_name) * 18)) / 2)
        selected_sensor_text.y = 55

        screen.append(selected_sensor_text)

        # Add butto text
        button_text_1 = label.Label(
            terminalio.FONT,
            text='Change\nModule',
            color=0xFFFFFF,
            scale=1
        )
        button_text_1.x = 10
        button_text_1.y = 100

        screen.append(button_text_1)

        button_text_2 = label.Label(
            terminalio.FONT,
            text='Change\nSensor',
            color=0xFFFFFF,
            scale=1
        )
        button_text_2.x = 80
        button_text_2.y = 100

        screen.append(button_text_2)

        button_text_3 = label.Label(
            terminalio.FONT,
            text='\nAccept',
            color=0xFFFFFF,
            scale=1
        )
        button_text_3.x = 230
        button_text_3.y = 100

        screen.append(button_text_3)

        display.show(screen)
        display.refresh()
        
        buttons = keypad.Keys((board.BUTTON_A, board.BUTTON_B, board.BUTTON_D), value_when_pressed=False, pull=True)
        time.sleep(display.time_to_refresh)

        event = None
        input_changed = False
        timeout = 60
        while input_changed == False and event == None:
            event = buttons.events.get()

            if timeout <= 0:
                buttons.deinit()
                return module, sensor

            if event:
                if event.pressed:
                    if event.key_number == 0:
                        input_changed == True
                        sensor = 0
                        if len(station) - 1 != module:
                            module += 1 
                        else:
                            module = 0
                        break
                    elif event.key_number == 1:
                        input_changed = True
                        if len(station[module]['sensors']) - 1 != sensor:
                            sensor += 1
                        else:
                            sensor = 0
                    elif event.key_number == 2:
                        buttons.deinit()
                        return module, sensor

            timeout -= 0.1
            time.sleep(0.1)
        buttons.deinit()
