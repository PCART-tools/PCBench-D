def _save(im, fp, filename):

    try:
        rawmode, bits, colormaptype, imagetype = SAVE[im.mode]
    except KeyError as e:
        raise OSError(f"cannot write mode {im.mode} as TGA") from e

    if "rle" in im.encoderinfo:
        rle = im.encoderinfo["rle"]
    else:
        compression = im.encoderinfo.get("compression", im.info.get("compression"))
        rle = compression == "tga_rle"
    if rle:
        imagetype += 8

    id_section = im.encoderinfo.get("id_section", im.info.get("id_section", ""))
    id_len = len(id_section)
    if id_len > 255:
        id_len = 255
        id_section = id_section[:255]
        warnings.warn("id_section has been trimmed to 255 characters")

    if colormaptype:
        colormapfirst, colormaplength, colormapentry = 0, 256, 24
    else:
        colormapfirst, colormaplength, colormapentry = 0, 0, 0

    if im.mode in ("LA", "RGBA"):
        flags = 8
    else:
        flags = 0

    orientation = im.encoderinfo.get("orientation", im.info.get("orientation", -1))
    if orientation > 0:
        flags = flags | 0x20

    fp.write(
        o8(id_len)
        + o8(colormaptype)
        + o8(imagetype)
        + o16(colormapfirst)
        + o16(colormaplength)
        + o8(colormapentry)
        + o16(0)
        + o16(0)
        + o16(im.size[0])
        + o16(im.size[1])
        + o8(bits)
        + o8(flags)
    )

    if id_section:
        fp.write(id_section)

    if colormaptype:
        fp.write(im.im.getpalette("RGB", "BGR"))

    if rle:
        ImageFile._save(
            im, fp, [("tga_rle", (0, 0) + im.size, 0, (rawmode, orientation))]
        )
    else:
        ImageFile._save(
            im, fp, [("raw", (0, 0) + im.size, 0, (rawmode, 0, orientation))]
        )

    # write targa version 2 footer
    fp.write(b"\000" * 8 + b"TRUEVISION-XFILE." + b"\000")
