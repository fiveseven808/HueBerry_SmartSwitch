import Adafruit_SSD1306
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

def string_width(fontType,string):
	string_width = 0

	for i, c in enumerate(string):
		char_width, char_height = draw.textsize(c, font=fontType)
		string_width += char_width

	return string_width
    
# 128x64 display with hardware I2C
disp = Adafruit_SSD1306.SSD1306_128_64(rst=24)
# Initialize library
disp.begin()
# Get display width and height
width = disp.width
height = disp.height
# Clear display
disp.clear()
disp.display()
# Create image buffer with mode '1' for 1-bit color
image = Image.new('1', (width, height))
# Load default font
font = ImageFont.load_default()
# Create drawing object
draw = ImageDraw.Draw(image)

#Clear Draw buffer
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Set font type and size
font = ImageFont.truetype('BMW_naa.ttf', 29)
#font = ImageFont.load_default()
# Set and Position splash
splash = "hueBerry"
x_pos = 2 + (disp.width/2)-(string_width(font,splash)/2)
y_pos = 8 + (disp.height-4-8)/2 - (35/2)

# Draw splash
draw.text((x_pos, y_pos), splash, font=font, fill=255)
disp.image(image)
disp.display()