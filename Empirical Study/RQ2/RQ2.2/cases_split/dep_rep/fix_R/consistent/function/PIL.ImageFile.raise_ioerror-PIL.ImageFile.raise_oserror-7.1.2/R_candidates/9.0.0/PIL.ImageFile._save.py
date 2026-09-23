def _save(im, fp, tile, bufsize=0):
    """Helper to save image based on tile list

    :param im: Image object.
    :param fp: File object.
    :param tile: Tile list.
    :param bufsize: Optional buffer size
    """

    im.load()
    if not hasattr(im, "encoderconfig"):
        im.encoderconfig = ()
    tile.sort(key=_tilesort)
    # FIXME: make MAXBLOCK a configuration parameter
    # It would be great if we could have the encoder specify what it needs
    # But, it would need at least the image size in most cases. RawEncode is
    # a tricky case.
    bufsize = max(MAXBLOCK, bufsize, im.size[0] * 4)  # see RawEncode.c
    try:
        fh = fp.fileno()
        fp.flush()
    except (AttributeError, io.UnsupportedOperation) as exc:
        # compress to Python file-compatible object
        for e, b, o, a in tile:
            e = Image._getencoder(im.mode, e, a, im.encoderconfig)
            if o > 0:
                fp.seek(o)
            e.setimage(im.im, b)
            if e.pushes_fd:
                e.setfd(fp)
                l, s = e.encode_to_pyfd()
            else:
                while True:
                    l, s, d = e.encode(bufsize)
                    fp.write(d)
                    if s:
                        break
            if s < 0:
                raise OSError(f"encoder error {s} when writing image file") from exc
            e.cleanup()
    else:
        # slight speedup: compress to real file object
        for e, b, o, a in tile:
            e = Image._getencoder(im.mode, e, a, im.encoderconfig)
            if o > 0:
                fp.seek(o)
            e.setimage(im.im, b)
            if e.pushes_fd:
                e.setfd(fp)
                l, s = e.encode_to_pyfd()
            else:
                s = e.encode_to_file(fh, bufsize)
            if s < 0:
                raise OSError(f"encoder error {s} when writing image file")
            e.cleanup()
    if hasattr(fp, "flush"):
        fp.flush()
