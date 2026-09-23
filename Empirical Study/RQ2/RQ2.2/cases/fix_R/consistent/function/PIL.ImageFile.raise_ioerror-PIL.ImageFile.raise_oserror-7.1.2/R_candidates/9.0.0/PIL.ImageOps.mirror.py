def mirror(image):
    """
    Flip image horizontally (left to right).

    :param image: The image to mirror.
    :return: An image.
    """
    return image.transpose(Image.FLIP_LEFT_RIGHT)
