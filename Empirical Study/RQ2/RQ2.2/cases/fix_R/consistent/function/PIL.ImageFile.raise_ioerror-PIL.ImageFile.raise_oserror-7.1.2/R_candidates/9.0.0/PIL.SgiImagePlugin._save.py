def _save(im, fp, filename):
    if im.mode != "RGB" and im.mode != "RGBA" and im.mode != "L":
        raise ValueError("Unsupported SGI image mode")

    # Get the keyword arguments
    info = im.encoderinfo

    # Byte-per-pixel precision, 1 = 8bits per pixel
    bpc = info.get("bpc", 1)

    if bpc not in (1, 2):
        raise ValueError("Unsupported number of bytes per pixel")

    # Flip the image, since the origin of SGI file is the bottom-left corner
    orientation = -1
    # Define the file as SGI File Format
    magicNumber = 474
    # Run-Length Encoding Compression - Unsupported at this time
    rle = 0

    # Number of dimensions (x,y,z)
    dim = 3
    # X Dimension = width / Y Dimension = height
    x, y = im.size
    if im.mode == "L" and y == 1:
        dim = 1
    elif im.mode == "L":
        dim = 2
    # Z Dimension: Number of channels
    z = len(im.mode)

    if dim == 1 or dim == 2:
        z = 1

    # assert we've got the right number of bands.
    if len(im.getbands()) != z:
        raise ValueError(
            f"incorrect number of bands in SGI write: {z} vs {len(im.getbands())}"
        )

    # Minimum Byte value
    pinmin = 0
    # Maximum Byte value (255 = 8bits per pixel)
    pinmax = 255
    # Image name (79 characters max, truncated below in write)
    imgName = os.path.splitext(os.path.basename(filename))[0]
    imgName = imgName.encode("ascii", "ignore")
    # Standard representation of pixel in the file
    colormap = 0
    fp.write(struct.pack(">h", magicNumber))
    fp.write(o8(rle))
    fp.write(o8(bpc))
    fp.write(struct.pack(">H", dim))
    fp.write(struct.pack(">H", x))
    fp.write(struct.pack(">H", y))
    fp.write(struct.pack(">H", z))
    fp.write(struct.pack(">l", pinmin))
    fp.write(struct.pack(">l", pinmax))
    fp.write(struct.pack("4s", b""))  # dummy
    fp.write(struct.pack("79s", imgName))  # truncates to 79 chars
    fp.write(struct.pack("s", b""))  # force null byte after imgname
    fp.write(struct.pack(">l", colormap))
    fp.write(struct.pack("404s", b""))  # dummy

    rawmode = "L"
    if bpc == 2:
        rawmode = "L;16B"

    for channel in im.split():
        fp.write(channel.tobytes("raw", rawmode, 0, orientation))

    if hasattr(fp, "flush"):
        fp.flush()
