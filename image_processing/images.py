from PIL import Image, ImageFilter


img = Image.open("images/bunny1.jpg")
print(img.format)
print(img.size)
print(img.mode)
print(dir(img))


filtered_img = img.filter(ImageFilter.BLUR)  # E.g. BLUR, SMOOTH, SHARPEN
filtered_img = img.convert("L")  # "L" corresponds to grayscale
filtered_img.rotate(90)
filtered_img.resize((300, 300))
filtered_img.crop((100,100,400,400))
filtered_img.show()
filtered_img.thumbnail((400,400))  # ".thumbnail" resizes the image to fit as much as possible, keeping the aspect ratio
filtered_img.save("formatted.png", "png")

