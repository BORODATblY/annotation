from PIL import Image
im = Image.open("lol.jpg")
nx, ny = im.size
scale = int (16)
im2 = im.resize((int(nx*scale), int(ny*scale)), Image.BICUBIC)
im2.save("x16.jpg", dpi=(19200, 19200), quality=90)