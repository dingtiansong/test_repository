#pip2 install pyocr
from PIL import Image
from pyocr import pyocr
 
tools = pyocr.get_available_tools()[:]
print("Using '%s'" % (tools[0].get_name()))
filePath = ['newImage/%r'%sss+'.png' for sss in range(12)]
for tmp in filePath:
    print tools[0].image_to_string(Image.open(tmp),lang='chi_sim')