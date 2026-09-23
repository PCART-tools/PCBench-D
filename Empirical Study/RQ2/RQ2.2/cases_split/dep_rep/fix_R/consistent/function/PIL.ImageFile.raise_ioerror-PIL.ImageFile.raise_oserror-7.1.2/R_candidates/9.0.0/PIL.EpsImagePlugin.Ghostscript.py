def Ghostscript(tile, size, fp, scale=1, transparency=False):
    """Render an image using Ghostscript"""

    # Unpack decoder tile
    decoder, tile, offset, data = tile[0]
    length, bbox = data

    # Hack to support hi-res rendering
    scale = int(scale) or 1
    # orig_size = size
    # orig_bbox = bbox
    size = (size[0] * scale, size[1] * scale)
    # resolution is dependent on bbox and size
    res = (
        72.0 * size[0] / (bbox[2] - bbox[0]),
        72.0 * size[1] / (bbox[3] - bbox[1]),
    )

    out_fd, outfile = tempfile.mkstemp()
    os.close(out_fd)

    infile_temp = None
    if hasattr(fp, "name") and os.path.exists(fp.name):
        infile = fp.name
    else:
        in_fd, infile_temp = tempfile.mkstemp()
        os.close(in_fd)
        infile = infile_temp

        # Ignore length and offset!
        # Ghostscript can read it
        # Copy whole file to read in Ghostscript
        with open(infile_temp, "wb") as f:
            # fetch length of fp
            fp.seek(0, io.SEEK_END)
            fsize = fp.tell()
            # ensure start position
            # go back
            fp.seek(0)
            lengthfile = fsize
            while lengthfile > 0:
                s = fp.read(min(lengthfile, 100 * 1024))
                if not s:
                    break
                lengthfile -= len(s)
                f.write(s)

    device = "pngalpha" if transparency else "ppmraw"

    # Build Ghostscript command
    command = [
        "gs",
        "-q",  # quiet mode
        "-g%dx%d" % size,  # set output geometry (pixels)
        "-r%fx%f" % res,  # set input DPI (dots per inch)
        "-dBATCH",  # exit after processing
        "-dNOPAUSE",  # don't pause between pages
        "-dSAFER",  # safe mode
        f"-sDEVICE={device}",
        f"-sOutputFile={outfile}",  # output file
        # adjust for image origin
        "-c",
        f"{-bbox[0]} {-bbox[1]} translate",
        "-f",
        infile,  # input file
        # showpage (see https://bugs.ghostscript.com/show_bug.cgi?id=698272)
        "-c",
        "showpage",
    ]

    if gs_windows_binary is not None:
        if not gs_windows_binary:
            raise OSError("Unable to locate Ghostscript on paths")
        command[0] = gs_windows_binary

    # push data through Ghostscript
    try:
        startupinfo = None
        if sys.platform.startswith("win"):
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.check_call(command, startupinfo=startupinfo)
        out_im = Image.open(outfile)
        out_im.load()
    finally:
        try:
            os.unlink(outfile)
            if infile_temp:
                os.unlink(infile_temp)
        except OSError:
            pass

    im = out_im.im.copy()
    out_im.close()
    return im
