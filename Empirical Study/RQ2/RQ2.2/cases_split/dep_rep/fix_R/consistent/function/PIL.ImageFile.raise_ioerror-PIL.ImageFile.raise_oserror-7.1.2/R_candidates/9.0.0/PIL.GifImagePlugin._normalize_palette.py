def _normalize_palette(im, palette, info):
    """
    Normalizes the palette for image.
      - Sets the palette to the incoming palette, if provided.
      - Ensures that there's a palette for L mode images
      - Optimizes the palette if necessary/desired.

    :param im: Image object
    :param palette: bytes object containing the source palette, or ....
    :param info: encoderinfo
    :returns: Image object
    """
    source_palette = None
    if palette:
        # a bytes palette
        if isinstance(palette, (bytes, bytearray, list)):
            source_palette = bytearray(palette[:768])
        if isinstance(palette, ImagePalette.ImagePalette):
            source_palette = bytearray(palette.palette)

    if im.mode == "P":
        if not source_palette:
            source_palette = im.im.getpalette("RGB")[:768]
    else:  # L-mode
        if not source_palette:
            source_palette = bytearray(i // 3 for i in range(768))
        im.palette = ImagePalette.ImagePalette("RGB", palette=source_palette)

    if palette:
        used_palette_colors = []
        for i in range(0, len(source_palette), 3):
            source_color = tuple(source_palette[i : i + 3])
            try:
                index = im.palette.colors[source_color]
            except KeyError:
                index = None
            used_palette_colors.append(index)
        for i, index in enumerate(used_palette_colors):
            if index is None:
                for j in range(len(used_palette_colors)):
                    if j not in used_palette_colors:
                        used_palette_colors[i] = j
                        break
        im = im.remap_palette(used_palette_colors)
    else:
        used_palette_colors = _get_optimize(im, info)
        if used_palette_colors is not None:
            return im.remap_palette(used_palette_colors, source_palette)

    im.palette.palette = source_palette
    return im
