from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

width = 128
height = 64
 
image = Image.new('1', (width, height))
# Load default font
font = ImageFont.load_default()
# Create drawing object
draw = ImageDraw.Draw(image)


def string_width(fontType,string):
    string_width = 0
    for i, c in enumerate(string):
        char_width, char_height = draw.textsize(c, font=fontType)
        string_width += char_width
    return string_width


text = "omgtest"
string_width(font,text)


def IntelliDraw(drawer,text,font,containerWidth):
    # Modified and stolen from https://mail.python.org/pipermail/image-sig/2004-December/003064.html
    # I'm not using it yet but this is some good inspiration
    words = text.split()  
    lines = [] # prepare a return argument
    lines.append(words) 
    finished = False
    line = 0
    while not finished:
        thistext = lines[line]
        newline = []
        innerFinished = False
        while not innerFinished:
            #print 'thistext: '+str(thistext)
            if drawer.textsize(' '.join(thistext),font)[0] > containerWidth:
                # this is the heart of the algorithm: we pop words off the current
                # sentence until the width is ok, then in the next outer loop
                # we move on to the next sentence. 
                newline.insert(0,thistext.pop(-1))
            else:
                innerFinished = True
        if len(newline) > 0:
            lines.append(newline)
            line = line + 1
        else:
            finished = True
    tmp = []        
    for i in lines:
        tmp.append( ' '.join(i) )
    lines = tmp
    (width,height) = drawer.textsize(lines[0],font)            
    total_height = len(lines)*(height+1)
    return (lines,width,height,total_height)
    
IntelliDraw(draw,"omg this is actually going to be a really long test sentence",font,width)

"""
code
text = 'One very extremely long string that cannot possibly fit \
into a small number of pixels of horizontal width, and the idea \
is to break this text up into multiple lines that can be placed like \
a paragraph into our image'

draw = ImageDraw.Draw(OurImagePreviouslyDefined)
font = fontpath = ImageFont.truetype('/usr/local/share/fonts/ttf/times.ttf',26)
pixelWidth = 500 # pixels

lines,tmp,h = IntelliDraw(draw,text,font,pixelWidth)
j = 0
for i in lines:
    draw.text( (0,0+j*h), i , font=font16, fill='black')
    j = j + 1
endcode
"""
