try:
    import Adafruit_SSD1306
except:
    print("splashscreen.py: Could not load requirements. Is this part of an import? ")
    exit()
from PIL import Image

# 128x64 display with hardware I2C
disp = Adafruit_SSD1306.SSD1306_128_64(rst=24)
# Initialize library.
try:
    disp.begin()
except:
    print("looks like this might be an spi display ")
    import Adafruit_GPIO.SPI as SPI
    RST = 24
    DC = 23
    SPI_PORT = 0
    SPI_DEVICE = 0
    disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))
    print("spi driver loaded instead")
    disp.begin()

# Clear display.
disp.clear()
disp.display()

#image = Image.open('happycat_oled_64.ppm').convert('1')
image = Image.open('hueberry_splash_64_bit.bmp').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
disp.image(image)
disp.display()
