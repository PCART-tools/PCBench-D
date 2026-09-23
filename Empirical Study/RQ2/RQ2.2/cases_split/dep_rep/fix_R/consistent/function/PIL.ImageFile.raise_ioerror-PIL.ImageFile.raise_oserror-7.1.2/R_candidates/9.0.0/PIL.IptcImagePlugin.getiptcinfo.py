def getiptcinfo(im):
    """
    Get IPTC information from TIFF, JPEG, or IPTC file.

    :param im: An image containing IPTC data.
    :returns: A dictionary containing IPTC information, or None if
        no IPTC information block was found.
    """
    import io

    from . import JpegImagePlugin, TiffImagePlugin

    data = None

    if isinstance(im, IptcImageFile):
        # return info dictionary right away
        return im.info

    elif isinstance(im, JpegImagePlugin.JpegImageFile):
        # extract the IPTC/NAA resource
        photoshop = im.info.get("photoshop")
        if photoshop:
            data = photoshop.get(0x0404)

    elif isinstance(im, TiffImagePlugin.TiffImageFile):
        # get raw data from the IPTC/NAA tag (PhotoShop tags the data
        # as 4-byte integers, so we cannot use the get method...)
        try:
            data = im.tag.tagdata[TiffImagePlugin.IPTC_NAA_CHUNK]
        except (AttributeError, KeyError):
            pass

    if data is None:
        return None  # no properties

    # create an IptcImagePlugin object without initializing it
    class FakeImage:
        pass

    im = FakeImage()
    im.__class__ = IptcImageFile

    # parse the IPTC information chunk
    im.info = {}
    im.fp = io.BytesIO(data)

    try:
        im._open()
    except (IndexError, KeyError):
        pass  # expected failure

    return im.info
