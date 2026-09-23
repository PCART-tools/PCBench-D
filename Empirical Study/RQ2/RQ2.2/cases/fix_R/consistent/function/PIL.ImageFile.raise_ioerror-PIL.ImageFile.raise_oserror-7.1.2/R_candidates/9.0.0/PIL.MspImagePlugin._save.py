def _save(im, fp, filename):

    if im.mode != "1":
        raise OSError(f"cannot write mode {im.mode} as MSP")

    # create MSP header
    header = [0] * 16

    header[0], header[1] = i16(b"Da"), i16(b"nM")  # version 1
    header[2], header[3] = im.size
    header[4], header[5] = 1, 1
    header[6], header[7] = 1, 1
    header[8], header[9] = im.size

    checksum = 0
    for h in header:
        checksum = checksum ^ h
    header[12] = checksum  # FIXME: is this the right field?

    # header
    for h in header:
        fp.write(o16(h))

    # image body
    ImageFile._save(im, fp, [("raw", (0, 0) + im.size, 32, ("1", 0, 1))])
