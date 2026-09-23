def get_interlace(im):
    interlace = im.encoderinfo.get("interlace", 1)

    # workaround for @PIL153
    if min(im.size) < 16:
        interlace = 0

    return interlace
