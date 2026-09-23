def jpeg_factory(fp=None, filename=None):
    im = JpegImageFile(fp, filename)
    try:
        mpheader = im._getmp()
        if mpheader[45057] > 1:
            # It's actually an MPO
            from .MpoImagePlugin import MpoImageFile

            # Don't reload everything, just convert it.
            im = MpoImageFile.adopt(im, mpheader)
    except (TypeError, IndexError):
        # It is really a JPEG
        pass
    except SyntaxError:
        warnings.warn(
            "Image appears to be a malformed MPO file, it will be "
            "interpreted as a base JPEG file"
        )
    return im
