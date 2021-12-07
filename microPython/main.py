import ssd1306
import machine
import utime as  time
import framebuf
import base64
import math
print("GurgleApps.com")

clockPin = 5
dataPin = 4
bus = 0
i2c = machine.I2C(bus,sda=machine.Pin(dataPin),scl=machine.Pin(clockPin))
display = ssd1306.SSD1306_I2C(128,64,i2c)
logoSmallB = b'aBn/gP//wH//4D//8B/w/AAf/gAP/wAH/4AD8MAAAeAAAPAAAHgAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAA4AAAAAAAOAAAAAACAOAAAAAAADgAAAAAAgCxAAAAAAHQAB4AMeIAscAAGMAB2AAeBPHiAJHsACmqAbwAGySBIhixLxwhr8H4ABEkgSIt8S+UIS3h+AARJIEiLfktsGE5IVIAFCSBoj2ZrbgoqSGYABckgeIhGe2MOOkgngATPIAiKQFthYBpIZgAEzwBIjgBD70ACSCYAB4AAaAQAQ0YAAEgmAAOAADgAAEMAAAAJpgAAAAAQAAADAAAAACADAAAHgAADwQAB4AAAw+AAP/AAH/gAD/wAB8P+A///Af//gP//wH/D////////////////w'
logoLargeB = b'gB//8A////AP///wD///8A///4AB//+AAf//gAH//4AB//wAAD/8AAA//AAAP/wAAD/gAAAH4AAAB+AAAAfgAAAHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHAAAAAAAAAAMAAAAAAAAAB4AAAAAAAAAHgAAAAAABgAeAAAAAAAAADwAAAAAAAYAFhgAAAAAAAHcAA4AAwZGADYYAAAHHAABwAAfAB8PxgA2HyAADz7AA94AH4CfjMYAMxswABs68AG8ABmMmQzGDiMZvBwYMvsA/QAZjJgMxh4/Gb4+GDP/g/wAMIyYDMYTPxmzNBgzz4B8ADCMmAzGN3sZszAZM8yDxQAwDJgExj5jmbM8GxPMgdwAM4yYB8YwYZ+zHh8fzMHdADPN2AfGMmAfswbMDszB3QARz9gAxjZgGzsmwADMwZ0AGY6ADMYeABg/PIAATMWdAB+AAATCGAAYNzgAAAzBnQAPgAAHwAAAGDAAAAAAxZ0ABwAAA8AAAAAwAAAAAA2cAAAAAAAAAAAAMAAAAAABgDgAAAH4AAAB+BAAAfgAAAH/AAAP/wAAD/8AAA//AAAP//AA///wAP//8AD///AA///+B////gf///4H///+B//'
logoPongB = b'gCz///////////////////////////////////////////wD8Pgf8D//AH/A/7wfgf/8APDwD8Af/wA/gHg8HwD//ABw4AeAD/8AHwA4HB4Af/wAcOAHgA//AA4AGBwcAH/8MHDggwAH/w4OABgcHAB//DgwwcMDB/8PDA4YDBg4P/w4MMPDB4f/DwweCAwYfD/8ODDDwweH/w8MHggEGHw//Dgww+cPh/8PDB8IBBj8P/w4MMP+D4P/DwwfCAQQ///8OHDD/g+CAQ4MPwwAMP///CBww/4PwgEEDD8MQDDAP/wAcMP+D4IBABw/DEAwwB/8APDD/w+CAQA8PwxgMMAf/APww+EPh/8AfB8MYDDgH/wf8MPhD4f/B/weCGAw+H/8P/DDww+H/wf8HghwMPh//D/wwcMHB/8H/h4YcDB4f/w/8OHDgA//B/4AGDg4MP/8P/DgA4AP/wf+ABg4OAD//D/w4AfAH/8H/wA4ODgA//wf8PAP4D//B/+AeDw8Af/8P//4H/j//wf/8/h//gP/////////////////////////////////////////////////////////////////////////////////////////////////////////////DnMD4c+Dh4ODwf4eHjx//gZzAcDPg4eBgYH8DA44f/xucxGNz5+HmZiP+NjGGH/8/nMZn8+fg5mYj/n5xhh//P5zEZ/PgxOZmIf5+eYYf/zGcwEYz4MzgYHD+fnmUn/8xnMDmM+HM4OD4fn55kJ//OZzE5zPnwGfn/H5+cZCf/xmIxGMx54Bn5/x+PjGRn/+BgMRgMCCMZ+fgZwIDmZ//gcHGcDAgjmfn4OcDB5mf///3//////////v/////////////////////////////////////////////////w=='
logoPongIB = b'gCwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP8DwfgD8AA/4A/AEPgfgAD/w8P8D/gAP/Af4fD4P8AA/+PH/h/8AD/4P/H4+H/gAP/jx/4f/AA//H/5+Pj/4ADz48ffP/4APHx/+fj4/+AA8fPPjz8+ADw8/Hn8+fHwAPHzzw8+HgA8PPh9/Png8ADx888PPh4APDz4ff754PAA8fPPBjweADw8+D3++cDwAPHzzwB8HwA8PPg9/vvAAADx488AfB9/vHzwPP/zwAAA9+PPAHwPf7788Dzv88/wAP/jzwB8H3+/+PA87/PP+AD/w88APB9/v/DwPOfzz/gA/wPPB7weAD/g+Dzn88f4APgDzwe8HgA+APh95/PB4ADwA88PPB4APgD4fePzweAA8APPjz4+AD4AeHnj8+HgAPADx48f/AA+AH/58fHzwADwA8f/H/wAPgB/+fHx/8AA8APH/g/4AD4AP/Hx8f/AAPgDw/wH8AA+AB/h8PD/gADwAAH4AcAAPgADAeAAfwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8Yz8HjB8eHx8PgHh4cOAAfmM/j8wfHh+fn4D8/HHgAORjO5yMGB4ZmdwByc554ADAYzmYDBgfGZncAYGOeeAAwGM7mAwfOxmZ3gGBhnngAM5jP7nMHzMfn48BgYZrYADOYz8ZzB4zHx8HgYGGb2AAxmM7GMwYP5gYA4GBjm9gAOZ3O5zOGH+YGAOBwc5uYAB+fzufz99zmBgfmP38ZmAAfj45j8/fcZgYHxj8+GZgAAAIAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=='
ziva = 'gDv/wP/zA4A3///A//ADAjP/8fAP/+CBHwPg8C//4AAfAQfgH+/8yA//B+AP//wAB///AD///4AH4/wAP///gAeBB+B////AA/8DwH///8AD/wAA////4APvAAD////gAYcAAP////AB/wAA////8AH/AAD////8Af8AAf////wB/wAB/////gD/AAH////8AP8AA/////8AfgAD/////gB8AAP/////gH8AA/////+APwAD/////8AAAAP/////wAAAB//////AAAAH/////8AAAAf/////4AAAB//////gAAAD//////AAAAf/////8AAAB//////wAAAH//////AAAAX/////8AAAAf/////wAAABAf////AAAAEA////8AAAAAA////wAAAAAD////AAAAA+P/t/8AAAAH4/+B/wAAAAf7/83/AAAAD/v/x/8AAAAP/////wAAAA//////AAAAWg////+AAABAB////4AAAEAD////gAAAQAP///+AAADAAP8d/4AAAMAA/5z/gAAAwAH/AH+AAADAA/8Af4AAAPAL/wA/gAAA8AP/AD+AAAD/H//AP4AAAP8f/0A/gAAA////4H+MAAD////g/4wAAP//////jgAA//////+KAAD//////4AAAP//////gAAA//////+IAAD//////4gAAP//////mAAA//////+YAAD//////4AAAP//////EAAA//z///8AAAD//v///wAAAH/8Y///EAAA//xn//8QAAD//DP//lAAAP/wM//+UAAA//+f//7wAAB//////vAAAD/////+8AAAP/////7wAABu//////AAAA//////8AAAN///+/3wAAAH/////fAEAAXwP/v/4AAAB2B/+//gBAAuAAP9/8AAAD4AAfn/wAwAPwCAH/kABAA/AoAf+wAMAD+C9Qf4AAwAH4L9B/gADAAPh/Yf+AAMAB+F9h/4AA8AD8B/P/AADgAPwH8/8AAPAA/g///wAA8AD+H///AAD4AP+O//4AAfAAf////gAB+AB////+AAH4AD////4AAfwAP////AED/AAf///8AQD8AA////gAAfgAD///+AAA+AAH///wAAX4AAP///AAAPgAA///8AAC8AAB///wAAPwAMH///AAX/ABgP/+4AAY8AHAP/vgAD/gAYAf+eAAP+ABwALv4AB/4AHAAD/AAH/gAcAAv8AAf+ABwAA/wAA/4AHPg//AAP/gAcAAPwAAPw=='


def custom_to_buff(data):
    width = data[0]
    height = data[1]
    fbuff = framebuf.FrameBuffer(data[2:],width,height, framebuf.MONO_HLSB)
    return fbuff
      
def show_image(image):
    display.blit(image, 0, 0)
    display.show()
    
logoSmallBuff = custom_to_buff(bytearray(base64.b64decode(logoSmallB)))
logoLargeBuff = custom_to_buff(bytearray(base64.b64decode(logoLargeB)))
logoPong = custom_to_buff(bytearray(base64.b64decode(logoPongB)))
logoPongI = custom_to_buff(bytearray(base64.b64decode(logoPongIB)))
ziva_image = custom_to_buff(bytearray(base64.b64decode(ziva)))


while True:
    display.fill(0)
    show_image(ziva_image )
    time.sleep(3)
    display.fill(0)
    show_image(logoPong)
    time.sleep(6)

 