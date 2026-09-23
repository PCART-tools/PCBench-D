def _save(im, fp, filename):

    try:
        version, bits, planes, rawmode = SAVE[im.mode]
    except KeyError as e:
        raise ValueError(f"Cannot save {im.mode} images as PCX") from e

    # bytes per plane
    stride = (im.size[0] * bits + 7) // 8
    # stride should be even
    stride += stride % 2
    # Stride needs to be kept in sync with the PcxEncode.c version.
    # Ideally it should be passed in in the state, but the bytes value
    # gets overwritten.

    logger.debug(
        "PcxImagePlugin._save: xwidth: %d, bits: %d, stride: %d",
        im.size[0],
        bits,
        stride,
    )

    # under windows, we could determine the current screen size with
    # "Image.core.display_mode()[1]", but I think that's overkill...

    screen = im.size

    dpi = 100, 100

    # PCX header
    fp.write(
        o8(10)
        + o8(version)
        + o8(1)
        + o8(bits)
        + o16(0)
        + o16(0)
        + o16(im.size[0] - 1)
        + o16(im.size[1] - 1)
        + o16(dpi[0])
        + o16(dpi[1])
        + b"\0" * 24
        + b"\xFF" * 24
        + b"\0"
        + o8(planes)
        + o16(stride)
        + o16(1)
        + o16(screen[0])
        + o16(screen[1])
        + b"\0" * 54
    )

    assert fp.tell() == 128

    ImageFile._save(im, fp, [("pcx", (0, 0) + im.size, 0, (rawmode, bits * planes))])

    if im.mode == "P":
        # colour palette
        fp.write(o8(12))
        fp.write(im.im.getpalette("RGB", "RGB"))  # 768 bytes
    elif im.mode == "L":
        # greyscale palette
        fp.write(o8(12))
        for i in range(256):
            fp.write(o8(i) * 3)
