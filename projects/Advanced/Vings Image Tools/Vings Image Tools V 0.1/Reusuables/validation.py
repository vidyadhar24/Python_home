# from features import compression

from features.compression import compress_app

images = compress_app.images_list


def validate_images():
    if not images:
        compress_app.are_valid_images = False
    else:
        compress_app.are_valid_images = True
