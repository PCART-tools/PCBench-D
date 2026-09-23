def _save(im, fp, filename):

    try:
        image_type, rawmode = SAVE[im.mode]
    except KeyError as e:
        raise ValueError(f"Cannot save {im.mode} images as IM") from e

    frames = im.encoderinfo.get("frames", 1)

    fp.write(f"Image type: {image_type} image\r\n".encode("ascii"))
    if filename:
        # Each line must be 100 characters or less,
        # or: SyntaxError("not an IM file")
        # 8 characters are used for "Name: " and "\r\n"
        # Keep just the filename, ditch the potentially overlong path
        name, ext = os.path.splitext(os.path.basename(filename))
        name = "".join([name[: 92 - len(ext)], ext])

        fp.write(f"Name: {name}\r\n".encode("ascii"))
    fp.write(("Image size (x*y): %d*%d\r\n" % im.size).encode("ascii"))
    fp.write(f"File size (no of images): {frames}\r\n".encode("ascii"))
    if im.mode in ["P", "PA"]:
        fp.write(b"Lut: 1\r\n")
    fp.write(b"\000" * (511 - fp.tell()) + b"\032")
    if im.mode in ["P", "PA"]:
        fp.write(im.im.getpalette("RGB", "RGB;L"))  # 768 bytes
    ImageFile._save(im, fp, [("raw", (0, 0) + im.size, 0, (rawmode, 0, -1))])
