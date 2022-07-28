# loading the blurred image as the background
image = Image.open(file_name)
image_resized = image.resize((550, 480), Image.ANTIALIAS)
image_resized.save('img.jpg')
# time.sleep(1)
canvas = tk.Canvas(frame_result, width=382, height=250)
canvas.place(x=50, y=0)
image_object = Image.open("img.jpg")
pimage = itk.PhotoImage(image=image_object)
root.pimage = pimage  # to avoid garbage collection of image
canvas.create_image(0, 0, image=pimage)

# tk.Label(root, image=pimage).pack()
# label_result.configure(image = pimage)
