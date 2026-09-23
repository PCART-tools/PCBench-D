def _save(im, fp, filename):
    lossless = im.encoderinfo.get("lossless", False)
    quality = im.encoderinfo.get("quality", 80)
    icc_profile = im.encoderinfo.get("icc_profile") or ""
    exif = im.encoderinfo.get("exif", "")
    if isinstance(exif, Image.Exif):
        exif = exif.tobytes()
    xmp = im.encoderinfo.get("xmp", "")
    method = im.encoderinfo.get("method", 4)

    if im.mode not in _VALID_WEBP_LEGACY_MODES:
        alpha = (
            "A" in im.mode
            or "a" in im.mode
            or (im.mode == "P" and "transparency" in im.info)
        )
        im = im.convert("RGBA" if alpha else "RGB")

    data = _webp.WebPEncode(
        im.tobytes(),
        im.size[0],
        im.size[1],
        lossless,
        float(quality),
        im.mode,
        icc_profile,
        method,
        exif,
        xmp,
    )
    if data is None:
        raise OSError("cannot write file as WebP (encoder returned None)")

    fp.write(data)
