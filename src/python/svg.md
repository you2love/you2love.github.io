# 生成svg图片
<!-- toc --> 


```python

import sys
import os
from PIL import Image


def convertPixel(r, g, b, a=1):
    color = "#%02X%02X%02X" % (r, g, b)
    opacity = a
    return (color, opacity)


for r in sys.argv[1:]:
    root, ext = os.path.splitext(r)

    image = Image.open(r)
    mode = image.mode
    pixels = image.load()
    width, height = image.size

    print(image.mode)

    if "RGB" in mode:
        output = f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'

        for r in range(height):
            for c in range(width):
                color, opacity = convertPixel(*pixels[c, r])
                output += f'<rect x="{c}" y="{r}" width="1" height="1" fill="{color}" fill-opacity="{opacity}"/>'

        output += "</svg>"

        with open(root + ".svg", "w") as f:
            f.write(output)
```
