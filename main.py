import time
import signal
from gfxhat import touch, lcd, backlight, fonts
from PIL import Image, ImageFont, ImageDraw
from util.CoinTracker import CoinTracker


# Array of crypto currencies to track
tracked_coins = ["BTC", "ETH", "DOGE", "LTC", "BCH"]

# Currency to compare crypto currencies with
comparison_currency = "USD"

tracker = CoinTracker(tracked_coins, comparison_currency)

led_states = [False for _ in range(6)]


def handler(ch, event):
    # Turn on led
    switch_led_state(ch)

    if (event == "press" and ch == 0):
        print("button press left top -> metric backwards",)
        tracker.change_metric("backwards")

    elif (event == "press" and ch == 1):
        print("button press left middle -> metric forward",)
        tracker.change_metric("forward")

    elif (event == "press" and ch == 2):
        print("button press left bottom -> metric home",)
        tracker.change_metric("home")

    elif (event == "press" and ch == 3):
        print("button press bottom left -> coin backwards",)

        tracker.change_page("backwards")

    elif (event == "press" and ch == 4):
        print("button press bottom middle -> coin home")
        tracker.change_page("home")

    elif (event == "press" and ch == 5):
        print("button press bottom right -> coin forward")
        tracker.change_page("forward")

    change_text()

    # Turn off led
    switch_led_state(ch)


def switch_led_state(ch):
    led_states[ch] = not led_states[ch]
    touch.set_led(ch, led_states[ch])
    if led_states[ch]:
        backlight.set_pixel(ch, 0, 255, 255)
    else:
        backlight.set_pixel(ch, 0, 255, 0)
    backlight.show()


def change_text():
    width, height = lcd.dimensions()

    image = Image.new('P', (width, height))

    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(fonts.PressStart2P, 8)

    text = tracker.display_text()

    h = font.getsize(text)[1]

    x = 0
    y = (height - h) // 2

    draw.text((x, y), text, 1, font)

    backlight.show()

    for x in range(128):
        for y in range(64):
            pixel = image.getpixel((x, y))
            lcd.set_pixel(x, y, pixel)

    lcd.show()


# Bind buttons to handler
for x in range(6):
    backlight.set_pixel(x, 0, 255, 0)
    touch.on(x, handler)


# Set first text
change_text()

try:
    signal.pause()
except KeyboardInterrupt:
    for x in range(6):
        backlight.set_pixel(x, 0, 0, 0)
        touch.set_led(x, 0)
    backlight.show()
    lcd.clear()
    lcd.show()
