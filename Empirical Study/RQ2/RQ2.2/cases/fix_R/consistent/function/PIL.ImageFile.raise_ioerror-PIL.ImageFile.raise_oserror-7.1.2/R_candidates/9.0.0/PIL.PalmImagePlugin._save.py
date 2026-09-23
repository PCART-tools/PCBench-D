def _save(im, fp, filename):

    if im.mode == "P":

        # we assume this is a color Palm image with the standard colormap,
        # unless the "info" dict has a "custom-colormap" field

        rawmode = "P"
        bpp = 8
        version = 1

    elif im.mode == "L":
        if im.encoderinfo.get("bpp") in (1, 2, 4):
            # this is 8-bit grayscale, so we shift it to get the high-order bits,
            # and invert it because
            # Palm does greyscale from white (0) to black (1)
            bpp = im.encoderinfo["bpp"]
            im = im.point(
                lambda x, shift=8 - bpp, maxval=(1 << bpp) - 1: maxval - (x >> shift)
            )
        elif im.info.get("bpp") in (1, 2, 4):
            # here we assume that even though the inherent mode is 8-bit grayscale,
            # only the lower bpp bits are significant.
            # We invert them to match the Palm.
            bpp = im.info["bpp"]
            im = im.point(lambda x, maxval=(1 << bpp) - 1: maxval - (x & maxval))
        else:
            raise OSError(f"cannot write mode {im.mode} as Palm")

        # we ignore the palette here
        im.mode = "P"
        rawmode = "P;" + str(bpp)
        version = 1

    elif im.mode == "1":

        # monochrome -- write it inverted, as is the Palm standard
        rawmode = "1;I"
        bpp = 1
        version = 0

    else:

        raise OSError(f"cannot write mode {im.mode} as Palm")

    #
    # make sure image data is available
    im.load()

    # write header

    cols = im.size[0]
    rows = im.size[1]

    rowbytes = int((cols + (16 // bpp - 1)) / (16 // bpp)) * 2
    transparent_index = 0
    compression_type = _COMPRESSION_TYPES["none"]

    flags = 0
    if im.mode == "P" and "custom-colormap" in im.info:
        flags = flags & _FLAGS["custom-colormap"]
        colormapsize = 4 * 256 + 2
        colormapmode = im.palette.mode
        colormap = im.getdata().getpalette()
    else:
        colormapsize = 0

    if "offset" in im.info:
        offset = (rowbytes * rows + 16 + 3 + colormapsize) // 4
    else:
        offset = 0

    fp.write(o16b(cols) + o16b(rows) + o16b(rowbytes) + o16b(flags))
    fp.write(o8(bpp))
    fp.write(o8(version))
    fp.write(o16b(offset))
    fp.write(o8(transparent_index))
    fp.write(o8(compression_type))
    fp.write(o16b(0))  # reserved by Palm

    # now write colormap if necessary

    if colormapsize > 0:
        fp.write(o16b(256))
        for i in range(256):
            fp.write(o8(i))
            if colormapmode == "RGB":
                fp.write(
                    o8(colormap[3 * i])
                    + o8(colormap[3 * i + 1])
                    + o8(colormap[3 * i + 2])
                )
            elif colormapmode == "RGBA":
                fp.write(
                    o8(colormap[4 * i])
                    + o8(colormap[4 * i + 1])
                    + o8(colormap[4 * i + 2])
                )

    # now convert data to raw form
    ImageFile._save(im, fp, [("raw", (0, 0) + im.size, 0, (rawmode, rowbytes, 1))])

    if hasattr(fp, "flush"):
        fp.flush()
