def _init_tests():
    # The version of FreeType to install locally for running the
    # tests.  This must match the value in `setupext.py`
    LOCAL_FREETYPE_VERSION = '2.6.1'

    from matplotlib import ft2font
    if (ft2font.__freetype_version__ != LOCAL_FREETYPE_VERSION or
            ft2font.__freetype_build_type__ != 'local'):
        _log.warning(
            f"Matplotlib is not built with the correct FreeType version to "
            f"run tests.  Rebuild without setting system_freetype=1 in "
            f"mplsetup.cfg.  Expect many image comparison failures below.  "
            f"Expected freetype version {LOCAL_FREETYPE_VERSION}.  "
            f"Found freetype version {ft2font.__freetype_version__}.  "
            "Freetype build type is {}local".format(
                "" if ft2font.__freetype_build_type__ == 'local' else "not "))
