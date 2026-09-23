def preinit():
    """Explicitly load standard file format drivers."""

    global _initialized
    if _initialized >= 1:
        return

    try:
        from . import BmpImagePlugin

        assert BmpImagePlugin
    except ImportError:
        pass
    try:
        from . import GifImagePlugin

        assert GifImagePlugin
    except ImportError:
        pass
    try:
        from . import JpegImagePlugin

        assert JpegImagePlugin
    except ImportError:
        pass
    try:
        from . import PpmImagePlugin

        assert PpmImagePlugin
    except ImportError:
        pass
    try:
        from . import PngImagePlugin

        assert PngImagePlugin
    except ImportError:
        pass
    # try:
    #     import TiffImagePlugin
    #     assert TiffImagePlugin
    # except ImportError:
    #     pass

    _initialized = 1
