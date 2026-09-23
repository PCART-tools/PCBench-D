def read_png_or_jpeg2000(fobj, start_length, size):
    (start, length) = start_length
    fobj.seek(start)
    sig = fobj.read(12)
    if sig[:8] == b"\x89PNG\x0d\x0a\x1a\x0a":
        fobj.seek(start)
        im = PngImagePlugin.PngImageFile(fobj)
        Image._decompression_bomb_check(im.size)
        return {"RGBA": im}
    elif (
        sig[:4] == b"\xff\x4f\xff\x51"
        or sig[:4] == b"\x0d\x0a\x87\x0a"
        or sig == b"\x00\x00\x00\x0cjP  \x0d\x0a\x87\x0a"
    ):
        if not enable_jpeg2k:
            raise ValueError(
                "Unsupported icon subimage format (rebuild PIL "
                "with JPEG 2000 support to fix this)"
            )
        # j2k, jpc or j2c
        fobj.seek(start)
        jp2kstream = fobj.read(length)
        f = io.BytesIO(jp2kstream)
        im = Jpeg2KImagePlugin.Jpeg2KImageFile(f)
        Image._decompression_bomb_check(im.size)
        if im.mode != "RGBA":
            im = im.convert("RGBA")
        return {"RGBA": im}
    else:
        raise ValueError("Unsupported icon subimage format")
