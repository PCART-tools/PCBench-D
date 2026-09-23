def flip(image):
    """
    Flip the image vertically (top to bottom).

    :param image: The image to flip.
    :return: An image.
    """
    return image.transpose(Image.FLIP_TOP_BOTTOM)
