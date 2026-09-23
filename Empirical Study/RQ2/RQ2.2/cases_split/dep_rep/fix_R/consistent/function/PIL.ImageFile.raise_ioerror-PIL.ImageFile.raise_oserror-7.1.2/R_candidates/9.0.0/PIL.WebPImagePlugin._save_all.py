def _save_all(im, fp, filename):
    encoderinfo = im.encoderinfo.copy()
    append_images = list(encoderinfo.get("append_images", []))

    # If total frame count is 1, then save using the legacy API, which
    # will preserve non-alpha modes
    total = 0
    for ims in [im] + append_images:
        total += getattr(ims, "n_frames", 1)
    if total == 1:
        _save(im, fp, filename)
        return

    background = (0, 0, 0, 0)
    if "background" in encoderinfo:
        background = encoderinfo["background"]
    elif "background" in im.info:
        background = im.info["background"]
        if isinstance(background, int):
            # GifImagePlugin stores a global color table index in
            # info["background"]. So it must be converted to an RGBA value
            palette = im.getpalette()
            if palette:
                r, g, b = palette[background * 3 : (background + 1) * 3]
                background = (r, g, b, 0)

    duration = im.encoderinfo.get("duration", im.info.get("duration"))
    loop = im.encoderinfo.get("loop", 0)
    minimize_size = im.encoderinfo.get("minimize_size", False)
    kmin = im.encoderinfo.get("kmin", None)
    kmax = im.encoderinfo.get("kmax", None)
    allow_mixed = im.encoderinfo.get("allow_mixed", False)
    verbose = False
    lossless = im.encoderinfo.get("lossless", False)
    quality = im.encoderinfo.get("quality", 80)
    method = im.encoderinfo.get("method", 0)
    icc_profile = im.encoderinfo.get("icc_profile") or ""
    exif = im.encoderinfo.get("exif", "")
    if isinstance(exif, Image.Exif):
        exif = exif.tobytes()
    xmp = im.encoderinfo.get("xmp", "")
    if allow_mixed:
        lossless = False

    # Sensible keyframe defaults are from gif2webp.c script
    if kmin is None:
        kmin = 9 if lossless else 3
    if kmax is None:
        kmax = 17 if lossless else 5

    # Validate background color
    if (
        not isinstance(background, (list, tuple))
        or len(background) != 4
        or not all(v >= 0 and v < 256 for v in background)
    ):
        raise OSError(
            "Background color is not an RGBA tuple clamped to (0-255): %s"
            % str(background)
        )

    # Convert to packed uint
    bg_r, bg_g, bg_b, bg_a = background
    background = (bg_a << 24) | (bg_r << 16) | (bg_g << 8) | (bg_b << 0)

    # Setup the WebP animation encoder
    enc = _webp.WebPAnimEncoder(
        im.size[0],
        im.size[1],
        background,
        loop,
        minimize_size,
        kmin,
        kmax,
        allow_mixed,
        verbose,
    )

    # Add each frame
    frame_idx = 0
    timestamp = 0
    cur_idx = im.tell()
    try:
        for ims in [im] + append_images:
            # Get # of frames in this image
            nfr = getattr(ims, "n_frames", 1)

            for idx in range(nfr):
                ims.seek(idx)
                ims.load()

                # Make sure image mode is supported
                frame = ims
                rawmode = ims.mode
                if ims.mode not in _VALID_WEBP_MODES:
                    alpha = (
                        "A" in ims.mode
                        or "a" in ims.mode
                        or (ims.mode == "P" and "A" in ims.im.getpalettemode())
                    )
                    rawmode = "RGBA" if alpha else "RGB"
                    frame = ims.convert(rawmode)

                if rawmode == "RGB":
                    # For faster conversion, use RGBX
                    rawmode = "RGBX"

                # Append the frame to the animation encoder
                enc.add(
                    frame.tobytes("raw", rawmode),
                    timestamp,
                    frame.size[0],
                    frame.size[1],
                    rawmode,
                    lossless,
                    quality,
                    method,
                )

                # Update timestamp and frame index
                if isinstance(duration, (list, tuple)):
                    timestamp += duration[frame_idx]
                else:
                    timestamp += duration
                frame_idx += 1

    finally:
        im.seek(cur_idx)

    # Force encoder to flush frames
    enc.add(None, timestamp, 0, 0, "", lossless, quality, 0)

    # Get the final output from the encoder
    data = enc.assemble(icc_profile, exif, xmp)
    if data is None:
        raise OSError("cannot write file as WebP (encoder returned None)")

    fp.write(data)
