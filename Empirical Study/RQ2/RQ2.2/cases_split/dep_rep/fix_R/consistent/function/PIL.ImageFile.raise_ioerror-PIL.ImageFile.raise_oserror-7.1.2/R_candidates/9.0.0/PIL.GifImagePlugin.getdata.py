def getdata(im, offset=(0, 0), **params):
    """
    Legacy Method

    Return a list of strings representing this image.
    The first string is a local image header, the rest contains
    encoded image data.

    :param im: Image object
    :param offset: Tuple of (x, y) pixels. Defaults to (0,0)
    :param \\**params: E.g. duration or other encoder info parameters
    :returns: List of Bytes containing gif encoded frame data

    """

    class Collector:
        data = []

        def write(self, data):
            self.data.append(data)

    im.load()  # make sure raster data is available

    fp = Collector()

    _write_frame_data(fp, im, offset, params)

    return fp.data
