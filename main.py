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
    print(ch)
    print(event)
    if event == 'press':
        led_states[ch] = not led_states[ch]
        touch.set_led(ch, led_states[ch])
        if led_states[ch]:
            backlight.set_pixel(ch, 0, 255, 255)
        else:
            backlight.set_pixel(ch, 0, 255, 0)
        backlight.show()

    if (event == "press" and ch == 0):
        print("button press left top")
        tracker.change_metric("backwards")

        print(ch, "done")

    elif (event == "press" and ch == 1):
        print("button press left middle -> metric forward")
        tracker.change_metric("forward")
        print(ch, "done")

    elif (event == "press" and ch == 2):
        print("button press left bottom -> metric home")
        tracker.change_metric("home")
        print(ch, "done")

    elif (event == "press" and ch == 3):
        print("button press bottom page left")
        tracker.change_page("backwards")
        print(ch, "done")

    elif (event == "press" and ch == 4):
        print("button press bottom middle -> page home")
        tracker.change_page("home")
        print(ch, "done")

    elif (event == "press" and ch == 5):

        print("button press bottom right -> change primary currency forward")
        tracker.change_page("forward")
        print(ch, "done")

    change_text()


def change_text():
    width, height = lcd.dimensions()

    image = Image.new('P', (width, height))

    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(fonts.AmaticSCBold, 16)

    text = tracker.display_text()

    w, h = font.getsize(text)

    x = (width - w) // 2
    y = (height - h) // 2

    draw.text((x, y), text, 1, font)

    backlight.show()

    for x in range(128):
        for y in range(64):
            pixel = image.getpixel((x, y))
            lcd.set_pixel(x, y, pixel)

    lcd.show()


# Button led
for x in range(6):
    touch.set_led(x, 1)
    time.sleep(0.1)
    touch.set_led(x, 0)

# Button
for x in range(6):
    backlight.set_pixel(x, 0, 255, 0)
    touch.on(x, handler)


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
