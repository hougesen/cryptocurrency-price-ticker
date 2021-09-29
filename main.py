from gfxhat import touch, lcd, backlight, fonts
from PIL import Image, ImageFont, ImageDraw
from util.CoinTracker import CoinTracker


# Array of crypto currencies to track
tracked_coins = ["BTC", "ETH", "DOGE", "LTC", "BCH"]

# Array of currencies to compare crypto currencies with
comparison_currencies = ["DKK", "USD", "BTC"]

test = CoinTracker(tracked_coins, comparison_currencies)


led_states = [False for _ in range(6)]

width, height = lcd.dimensions()

image = Image.new('P', (width, height))

draw = ImageDraw.Draw(image)

font = ImageFont.truetype(fonts.AmaticSCBold, 38)

text = "{coin_symbol} - {coin_price}".format(
    coin_symbol=test.current_coin["symbol"], coin_price=test.current_coin["price"]
)


w, h = font.getsize(text)

x = (width - w) // 2
y = (height - h) // 2

draw.text((x, y), text, 1, font)


def handler(ch, event):
    if event == 'press':
        led_states[ch] = not led_states[ch]
        touch.set_led(ch, led_states[ch])
        if led_states[ch]:
            backlight.set_pixel(ch, 0, 255, 255)
        else:
            backlight.set_pixel(ch, 0, 255, 0)
        backlight.show()


for x in range(6):
    touch.set_led(x, 1)
    time.sleep(0.1)
    touch.set_led(x, 0)

for x in range(6):
    backlight.set_pixel(x, 0, 255, 0)
    touch.on(x, handler)

backlight.show()

for x in range(128):
    for y in range(64):
        pixel = image.getpixel((x, y))
        lcd.set_pixel(x, y, pixel)


lcd.show()

try:
    signal.pause()
except KeyboardInterrupt:
    for x in range(6):
        backlight.set_pixel(x, 0, 0, 0)
        touch.set_led(x, 0)
    backlight.show()
    lcd.clear()
    lcd.show()
