def _save(im, fp, filename):

    try:
        rawmode = RAWMODE[im.mode]
    except KeyError as e:
        raise OSError(f"cannot write mode {im.mode} as JPEG") from e

    info = im.encoderinfo

    dpi = [round(x) for x in info.get("dpi", (0, 0))]

    quality = info.get("quality", -1)
    subsampling = info.get("subsampling", -1)
    qtables = info.get("qtables")

    if quality == "keep":
        quality = -1
        subsampling = "keep"
        qtables = "keep"
    elif quality in presets:
        preset = presets[quality]
        quality = -1
        subsampling = preset.get("subsampling", -1)
        qtables = preset.get("quantization")
    elif not isinstance(quality, int):
        raise ValueError("Invalid quality setting")
    else:
        if subsampling in presets:
            subsampling = presets[subsampling].get("subsampling", -1)
        if isinstance(qtables, str) and qtables in presets:
            qtables = presets[qtables].get("quantization")

    if subsampling == "4:4:4":
        subsampling = 0
    elif subsampling == "4:2:2":
        subsampling = 1
    elif subsampling == "4:2:0":
        subsampling = 2
    elif subsampling == "4:1:1":
        # For compatibility. Before Pillow 4.3, 4:1:1 actually meant 4:2:0.
        # Set 4:2:0 if someone is still using that value.
        subsampling = 2
    elif subsampling == "keep":
        if im.format != "JPEG":
            raise ValueError("Cannot use 'keep' when original image is not a JPEG")
        subsampling = get_sampling(im)

    def validate_qtables(qtables):
        if qtables is None:
            return qtables
        if isinstance(qtables, str):
            try:
                lines = [
                    int(num)
                    for line in qtables.splitlines()
                    for num in line.split("#", 1)[0].split()
                ]
            except ValueError as e:
                raise ValueError("Invalid quantization table") from e
            else:
                qtables = [lines[s : s + 64] for s in range(0, len(lines), 64)]
        if isinstance(qtables, (tuple, list, dict)):
            if isinstance(qtables, dict):
                qtables = [
                    qtables[key] for key in range(len(qtables)) if key in qtables
                ]
            elif isinstance(qtables, tuple):
                qtables = list(qtables)
            if not (0 < len(qtables) < 5):
                raise ValueError("None or too many quantization tables")
            for idx, table in enumerate(qtables):
                try:
                    if len(table) != 64:
                        raise TypeError
                    table = array.array("H", table)
                except TypeError as e:
                    raise ValueError("Invalid quantization table") from e
                else:
                    qtables[idx] = list(table)
            return qtables

    if qtables == "keep":
        if im.format != "JPEG":
            raise ValueError("Cannot use 'keep' when original image is not a JPEG")
        qtables = getattr(im, "quantization", None)
    qtables = validate_qtables(qtables)

    extra = b""

    icc_profile = info.get("icc_profile")
    if icc_profile:
        ICC_OVERHEAD_LEN = 14
        MAX_BYTES_IN_MARKER = 65533
        MAX_DATA_BYTES_IN_MARKER = MAX_BYTES_IN_MARKER - ICC_OVERHEAD_LEN
        markers = []
        while icc_profile:
            markers.append(icc_profile[:MAX_DATA_BYTES_IN_MARKER])
            icc_profile = icc_profile[MAX_DATA_BYTES_IN_MARKER:]
        i = 1
        for marker in markers:
            size = struct.pack(">H", 2 + ICC_OVERHEAD_LEN + len(marker))
            extra += (
                b"\xFF\xE2"
                + size
                + b"ICC_PROFILE\0"
                + o8(i)
                + o8(len(markers))
                + marker
            )
            i += 1

    # "progressive" is the official name, but older documentation
    # says "progression"
    # FIXME: issue a warning if the wrong form is used (post-1.1.7)
    progressive = info.get("progressive", False) or info.get("progression", False)

    optimize = info.get("optimize", False)

    exif = info.get("exif", b"")
    if isinstance(exif, Image.Exif):
        exif = exif.tobytes()

    # get keyword arguments
    im.encoderconfig = (
        quality,
        progressive,
        info.get("smooth", 0),
        optimize,
        info.get("streamtype", 0),
        dpi[0],
        dpi[1],
        subsampling,
        qtables,
        extra,
        exif,
    )

    # if we optimize, libjpeg needs a buffer big enough to hold the whole image
    # in a shot. Guessing on the size, at im.size bytes. (raw pixel size is
    # channels*size, this is a value that's been used in a django patch.
    # https://github.com/matthewwithanm/django-imagekit/issues/50
    bufsize = 0
    if optimize or progressive:
        # CMYK can be bigger
        if im.mode == "CMYK":
            bufsize = 4 * im.size[0] * im.size[1]
        # keep sets quality to -1, but the actual value may be high.
        elif quality >= 95 or quality == -1:
            bufsize = 2 * im.size[0] * im.size[1]
        else:
            bufsize = im.size[0] * im.size[1]

    # The EXIF info needs to be written as one block, + APP1, + one spare byte.
    # Ensure that our buffer is big enough. Same with the icc_profile block.
    bufsize = max(ImageFile.MAXBLOCK, bufsize, len(exif) + 5, len(extra) + 1)

    ImageFile._save(im, fp, [("jpeg", (0, 0) + im.size, 0, rawmode)], bufsize)
