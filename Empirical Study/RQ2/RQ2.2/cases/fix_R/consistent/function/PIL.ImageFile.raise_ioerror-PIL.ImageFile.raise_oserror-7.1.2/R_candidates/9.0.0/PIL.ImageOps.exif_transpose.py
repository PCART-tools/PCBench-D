def exif_transpose(image):
    """
    If an image has an EXIF Orientation tag, return a new image that is
    transposed accordingly. Otherwise, return a copy of the image.

    :param image: The image to transpose.
    :return: An image.
    """
    exif = image.getexif()
    orientation = exif.get(0x0112)
    method = {
        2: Image.FLIP_LEFT_RIGHT,
        3: Image.ROTATE_180,
        4: Image.FLIP_TOP_BOTTOM,
        5: Image.TRANSPOSE,
        6: Image.ROTATE_270,
        7: Image.TRANSVERSE,
        8: Image.ROTATE_90,
    }.get(orientation)
    if method is not None:
        transposed_image = image.transpose(method)
        transposed_exif = transposed_image.getexif()
        if 0x0112 in transposed_exif:
            del transposed_exif[0x0112]
            if "exif" in transposed_image.info:
                transposed_image.info["exif"] = transposed_exif.tobytes()
            elif "Raw profile type exif" in transposed_image.info:
                transposed_image.info[
                    "Raw profile type exif"
                ] = transposed_exif.tobytes().hex()
            elif "XML:com.adobe.xmp" in transposed_image.info:
                transposed_image.info["XML:com.adobe.xmp"] = re.sub(
                    r'tiff:Orientation="([0-9])"',
                    "",
                    transposed_image.info["XML:com.adobe.xmp"],
                )
        return transposed_image
    return image.copy()
