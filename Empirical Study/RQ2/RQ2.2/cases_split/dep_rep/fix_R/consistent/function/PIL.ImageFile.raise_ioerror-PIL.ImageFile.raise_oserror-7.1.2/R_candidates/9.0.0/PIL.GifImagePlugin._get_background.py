def _get_background(im, infoBackground):
    background = 0
    if infoBackground:
        background = infoBackground
        if isinstance(background, tuple):
            # WebPImagePlugin stores an RGBA value in info["background"]
            # So it must be converted to the same format as GifImagePlugin's
            # info["background"] - a global color table index
            try:
                background = im.palette.getcolor(background, im)
            except ValueError as e:
                if str(e) == "cannot allocate more than 256 colors":
                    # If all 256 colors are in use,
                    # then there is no need for the background color
                    return 0
                else:
                    raise
    return background
