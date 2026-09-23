def _get_optimize(im, info):
    """
    Palette optimization is a potentially expensive operation.

    This function determines if the palette should be optimized using
    some heuristics, then returns the list of palette entries in use.

    :param im: Image object
    :param info: encoderinfo
    :returns: list of indexes of palette entries in use, or None
    """
    if im.mode in ("P", "L") and info and info.get("optimize", 0):
        # Potentially expensive operation.

        # The palette saves 3 bytes per color not used, but palette
        # lengths are restricted to 3*(2**N) bytes. Max saving would
        # be 768 -> 6 bytes if we went all the way down to 2 colors.
        # * If we're over 128 colors, we can't save any space.
        # * If there aren't any holes, it's not worth collapsing.
        # * If we have a 'large' image, the palette is in the noise.

        # create the new palette if not every color is used
        optimise = _FORCE_OPTIMIZE or im.mode == "L"
        if optimise or im.width * im.height < 512 * 512:
            # check which colors are used
            used_palette_colors = []
            for i, count in enumerate(im.histogram()):
                if count:
                    used_palette_colors.append(i)

            if optimise or (
                len(used_palette_colors) <= 128
                and max(used_palette_colors) > len(used_palette_colors)
            ):
                return used_palette_colors
