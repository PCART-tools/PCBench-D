def getchunks(im, **params):
    """Return a list of PNG chunks representing this image."""

    class collector:
        data = []

        def write(self, data):
            pass

        def append(self, chunk):
            self.data.append(chunk)

    def append(fp, cid, *data):
        data = b"".join(data)
        crc = o32(_crc32(data, _crc32(cid)))
        fp.append((cid, data, crc))

    fp = collector()

    try:
        im.encoderinfo = params
        _save(im, fp, None, append)
    finally:
        del im.encoderinfo

    return fp.data
