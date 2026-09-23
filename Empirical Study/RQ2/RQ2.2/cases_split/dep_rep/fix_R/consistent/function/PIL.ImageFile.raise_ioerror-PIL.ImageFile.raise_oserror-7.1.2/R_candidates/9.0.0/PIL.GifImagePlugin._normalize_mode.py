def _normalize_mode(im, initial_call=False):
    """
    Takes an image (or frame), returns an image in a mode that is appropriate
    for saving in a Gif.

    It may return the original image, or it may return an image converted to
    palette or 'L' mode.

    UNDONE: What is the point of mucking with the initial call palette, for
    an image that shouldn't have a palette, or it would be a mode 'P' and
    get returned in the RAWMODE clause.

    :param im: Image object
    :param initial_call: Default false, set to true for a single frame.
    :returns: Image object
    """
    if im.mode in RAWMODE:
        im.load()
        return im
    if Image.getmodebase(im.mode) == "RGB":
        if initial_call:
            palette_size = 256
            if im.palette:
                palette_size = len(im.palette.getdata()[1]) // 3
            im = im.convert("P", palette=Image.ADAPTIVE, colors=palette_size)
            if im.palette.mode == "RGBA":
                for rgba in im.palette.colors.keys():
                    if rgba[3] == 0:
                        im.info["transparency"] = im.palette.colors[rgba]
                        break
            return im
        else:
            return im.convert("P")
    return im.convert("L")
