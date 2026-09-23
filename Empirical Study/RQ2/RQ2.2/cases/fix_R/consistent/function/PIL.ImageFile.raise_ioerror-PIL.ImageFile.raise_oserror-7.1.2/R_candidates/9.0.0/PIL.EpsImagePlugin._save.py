def _save(im, fp, filename, eps=1):
    """EPS Writer for the Python Imaging Library."""

    #
    # make sure image data is available
    im.load()

    #
    # determine PostScript image mode
    if im.mode == "L":
        operator = (8, 1, b"image")
    elif im.mode == "RGB":
        operator = (8, 3, b"false 3 colorimage")
    elif im.mode == "CMYK":
        operator = (8, 4, b"false 4 colorimage")
    else:
        raise ValueError("image mode is not supported")

    if eps:
        #
        # write EPS header
        fp.write(b"%!PS-Adobe-3.0 EPSF-3.0\n")
        fp.write(b"%%Creator: PIL 0.1 EpsEncode\n")
        # fp.write("%%CreationDate: %s"...)
        fp.write(b"%%%%BoundingBox: 0 0 %d %d\n" % im.size)
        fp.write(b"%%Pages: 1\n")
        fp.write(b"%%EndComments\n")
        fp.write(b"%%Page: 1 1\n")
        fp.write(b"%%ImageData: %d %d " % im.size)
        fp.write(b'%d %d 0 1 1 "%s"\n' % operator)

    #
    # image header
    fp.write(b"gsave\n")
    fp.write(b"10 dict begin\n")
    fp.write(b"/buf %d string def\n" % (im.size[0] * operator[1]))
    fp.write(b"%d %d scale\n" % im.size)
    fp.write(b"%d %d 8\n" % im.size)  # <= bits
    fp.write(b"[%d 0 0 -%d 0 %d]\n" % (im.size[0], im.size[1], im.size[1]))
    fp.write(b"{ currentfile buf readhexstring pop } bind\n")
    fp.write(operator[2] + b"\n")
    if hasattr(fp, "flush"):
        fp.flush()

    ImageFile._save(im, fp, [("eps", (0, 0) + im.size, 0, None)])

    fp.write(b"\n%%%%EndBinary\n")
    fp.write(b"grestore end\n")
    if hasattr(fp, "flush"):
        fp.flush()
