def _save(im, fp, filename, chunk=putchunk, save_all=False):
    # save an image to disk (called by the save method)

    mode = im.mode

    if mode == "P":

        #
        # attempt to minimize storage requirements for palette images
        if "bits" in im.encoderinfo:
            # number of bits specified by user
            colors = min(1 << im.encoderinfo["bits"], 256)
        else:
            # check palette contents
            if im.palette:
                colors = max(min(len(im.palette.getdata()[1]) // 3, 256), 1)
            else:
                colors = 256

        if colors <= 16:
            if colors <= 2:
                bits = 1
            elif colors <= 4:
                bits = 2
            else:
                bits = 4
            mode = f"{mode};{bits}"

    # encoder options
    im.encoderconfig = (
        im.encoderinfo.get("optimize", False),
        im.encoderinfo.get("compress_level", -1),
        im.encoderinfo.get("compress_type", -1),
        im.encoderinfo.get("dictionary", b""),
    )

    # get the corresponding PNG mode
    try:
        rawmode, mode = _OUTMODES[mode]
    except KeyError as e:
        raise OSError(f"cannot write mode {mode} as PNG") from e

    #
    # write minimal PNG file

    fp.write(_MAGIC)

    chunk(
        fp,
        b"IHDR",
        o32(im.size[0]),  # 0: size
        o32(im.size[1]),
        mode,  # 8: depth/type
        b"\0",  # 10: compression
        b"\0",  # 11: filter category
        b"\0",  # 12: interlace flag
    )

    chunks = [b"cHRM", b"gAMA", b"sBIT", b"sRGB", b"tIME"]

    icc = im.encoderinfo.get("icc_profile", im.info.get("icc_profile"))
    if icc:
        # ICC profile
        # according to PNG spec, the iCCP chunk contains:
        # Profile name  1-79 bytes (character string)
        # Null separator        1 byte (null character)
        # Compression method    1 byte (0)
        # Compressed profile    n bytes (zlib with deflate compression)
        name = b"ICC Profile"
        data = name + b"\0\0" + zlib.compress(icc)
        chunk(fp, b"iCCP", data)

        # You must either have sRGB or iCCP.
        # Disallow sRGB chunks when an iCCP-chunk has been emitted.
        chunks.remove(b"sRGB")

    info = im.encoderinfo.get("pnginfo")
    if info:
        chunks_multiple_allowed = [b"sPLT", b"iTXt", b"tEXt", b"zTXt"]
        for info_chunk in info.chunks:
            cid, data = info_chunk[:2]
            if cid in chunks:
                chunks.remove(cid)
                chunk(fp, cid, data)
            elif cid in chunks_multiple_allowed:
                chunk(fp, cid, data)
            elif cid[1:2].islower():
                # Private chunk
                after_idat = info_chunk[2:3]
                if not after_idat:
                    chunk(fp, cid, data)

    if im.mode == "P":
        palette_byte_number = colors * 3
        palette_bytes = im.im.getpalette("RGB")[:palette_byte_number]
        while len(palette_bytes) < palette_byte_number:
            palette_bytes += b"\0"
        chunk(fp, b"PLTE", palette_bytes)

    transparency = im.encoderinfo.get("transparency", im.info.get("transparency", None))

    if transparency or transparency == 0:
        if im.mode == "P":
            # limit to actual palette size
            alpha_bytes = colors
            if isinstance(transparency, bytes):
                chunk(fp, b"tRNS", transparency[:alpha_bytes])
            else:
                transparency = max(0, min(255, transparency))
                alpha = b"\xFF" * transparency + b"\0"
                chunk(fp, b"tRNS", alpha[:alpha_bytes])
        elif im.mode in ("1", "L", "I"):
            transparency = max(0, min(65535, transparency))
            chunk(fp, b"tRNS", o16(transparency))
        elif im.mode == "RGB":
            red, green, blue = transparency
            chunk(fp, b"tRNS", o16(red) + o16(green) + o16(blue))
        else:
            if "transparency" in im.encoderinfo:
                # don't bother with transparency if it's an RGBA
                # and it's in the info dict. It's probably just stale.
                raise OSError("cannot use transparency for this mode")
    else:
        if im.mode == "P" and im.im.getpalettemode() == "RGBA":
            alpha = im.im.getpalette("RGBA", "A")
            alpha_bytes = colors
            chunk(fp, b"tRNS", alpha[:alpha_bytes])

    dpi = im.encoderinfo.get("dpi")
    if dpi:
        chunk(
            fp,
            b"pHYs",
            o32(int(dpi[0] / 0.0254 + 0.5)),
            o32(int(dpi[1] / 0.0254 + 0.5)),
            b"\x01",
        )

    if info:
        chunks = [b"bKGD", b"hIST"]
        for info_chunk in info.chunks:
            cid, data = info_chunk[:2]
            if cid in chunks:
                chunks.remove(cid)
                chunk(fp, cid, data)

    exif = im.encoderinfo.get("exif", im.info.get("exif"))
    if exif:
        if isinstance(exif, Image.Exif):
            exif = exif.tobytes(8)
        if exif.startswith(b"Exif\x00\x00"):
            exif = exif[6:]
        chunk(fp, b"eXIf", exif)

    if save_all:
        _write_multiple_frames(im, fp, chunk, rawmode)
    else:
        ImageFile._save(im, _idat(fp, chunk), [("zip", (0, 0) + im.size, 0, rawmode)])

    if info:
        for info_chunk in info.chunks:
            cid, data = info_chunk[:2]
            if cid[1:2].islower():
                # Private chunk
                after_idat = info_chunk[2:3]
                if after_idat:
                    chunk(fp, cid, data)

    chunk(fp, b"IEND", b"")

    if hasattr(fp, "flush"):
        fp.flush()
