import Adafruit_SSD1306
from PIL import Image
    
# 128x64 display with hardware I2C
disp = Adafruit_SSD1306.SSD1306_128_64(rst=24)
# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

#image = Image.open('happycat_oled_64.ppm').convert('1')
image = Image.open('hueberry_splash_64_bit.bmp').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
disp.image(image)
disp.display()
