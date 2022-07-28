import tinify as tf
with open('key.txt') as file:
    key = file.read()

tf.key = key
# compressing using image directly

# source =tf.from_file('Resources\\avi-richards.jpg')
# source.to_file('compreesed.jpg')

#compressing using image as binary data

with open('Resources\\avi-richards.jpg','rb') as file:
    source_image_data = file.read()

compressed_data = tf.from_buffer(source_image_data).to_buffer()

with open('compressed.jpg','wb') as file:
    file.write(compressed_data)
print("completed")

