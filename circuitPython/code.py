import board
import time
import adafruit_displayio_ssd1306
import displayio
import busio
import base64

logo_large = b'gB//8A////AP///wD///8A///4AB//+AAf//gAH//4AB//wAAD/8AAA//AAAP/wAAD/gAAAH4AAAB+AAAAfgAAAHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHAAAAAAAAAAMAAAAAAAAAB4AAAAAAAAAHgAAAAAABgAeAAAAAAAAADwAAAAAAAYAFhgAAAAAAAHcAA4AAwZGADYYAAAHHAABwAAfAB8PxgA2HyAADz7AA94AH4CfjMYAMxswABs68AG8ABmMmQzGDiMZvBwYMvsA/QAZjJgMxh4/Gb4+GDP/g/wAMIyYDMYTPxmzNBgzz4B8ADCMmAzGN3sZszAZM8yDxQAwDJgExj5jmbM8GxPMgdwAM4yYB8YwYZ+zHh8fzMHdADPN2AfGMmAfswbMDszB3QARz9gAxjZgGzsmwADMwZ0AGY6ADMYeABg/PIAATMWdAB+AAATCGAAYNzgAAAzBnQAPgAAHwAAAGDAAAAAAxZ0ABwAAA8AAAAAwAAAAAA2cAAAAAAAAAAAAMAAAAAABgDgAAAH4AAAB+BAAAfgAAAH/AAAP/wAAD/8AAA//AAAP//AA///wAP//8AD///AA///+B////gf///4H///+B//'
pong = b'gCwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP8DwfgD8AA/4A/AEPgfgAD/w8P8D/gAP/Af4fD4P8AA/+PH/h/8AD/4P/H4+H/gAP/jx/4f/AA//H/5+Pj/4ADz48ffP/4APHx/+fj4/+AA8fPPjz8+ADw8/Hn8+fHwAPHzzw8+HgA8PPh9/Png8ADx888PPh4APDz4ff754PAA8fPPBjweADw8+D3++cDwAPHzzwB8HwA8PPg9/vvAAADx488AfB9/vHzwPP/zwAAA9+PPAHwPf7788Dzv88/wAP/jzwB8H3+/+PA87/PP+AD/w88APB9/v/DwPOfzz/gA/wPPB7weAD/g+Dzn88f4APgDzwe8HgA+APh95/PB4ADwA88PPB4APgD4fePzweAA8APPjz4+AD4AeHnj8+HgAPADx48f/AA+AH/58fHzwADwA8f/H/wAPgB/+fHx/8AA8APH/g/4AD4AP/Hx8f/AAPgDw/wH8AA+AB/h8PD/gADwAAH4AcAAPgADAeAAfwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8Yz8HjB8eHx8PgHh4cOAAfmM/j8wfHh+fn4D8/HHgAORjO5yMGB4ZmdwByc554ADAYzmYDBgfGZncAYGOeeAAwGM7mAwfOxmZ3gGBhnngAM5jP7nMHzMfn48BgYZrYADOYz8ZzB4zHx8HgYGGb2AAxmM7GMwYP5gYA4GBjm9gAOZ3O5zOGH+YGAOBwc5uYAB+fzufz99zmBgfmP38ZmAAfj45j8/fcZgYHxj8+GZgAAAIAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=='

displayio.release_displays()
sda = board.GP4
scl = board.GP5
i2c = busio.I2C(scl, sda)
if(i2c.try_lock()):
    print("i2c.scan(): " + str(i2c.scan()))
    i2c.unlock()
ssd1306_i2c_addr = 0x3C
display_width =128
display_height = 64
NUM_OF_COLOR = 2

display_bus = displayio.I2CDisplay(i2c, device_address=ssd1306_i2c_addr)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=display_width, height=display_height)
bitmap_palette = displayio.Palette(NUM_OF_COLOR)
bitmap_palette[0] = 0x000000
bitmap_palette[1] = 0xFFFFFF

def custom_to_bitmap(custom):
    data = base64.b64decode(custom)
    b_width = data[0]
    b_height = data[1]
    row = 0
    col = 0
    bitmap = displayio.Bitmap(b_width, b_height, 2)
    for pix in data[2:]:
        for bit in range(8):
            bitmap[col+bit,row]=(pix>>(7-bit))&1
        col=col+8
        if col>=b_width-1:
            row=row+1
            col=0
    return bitmap

logo_bitmap = custom_to_bitmap(logo_large)
logo_group = displayio.Group()
logo_tile_grid = displayio.TileGrid(logo_bitmap,
                              pixel_shader=bitmap_palette,
                              x=0, y=0)
logo_group.append(logo_tile_grid)

pong_bitmap = custom_to_bitmap(pong)
pong_group = displayio.Group()
pong_tile_grid = displayio.TileGrid(pong_bitmap,
                              pixel_shader=bitmap_palette,
                              x=0, y=0)
pong_group.append(pong_tile_grid)

while True:
    display.show(logo_group)
    time.sleep(2)
    display.show(pong_group)
    time.sleep(2)

