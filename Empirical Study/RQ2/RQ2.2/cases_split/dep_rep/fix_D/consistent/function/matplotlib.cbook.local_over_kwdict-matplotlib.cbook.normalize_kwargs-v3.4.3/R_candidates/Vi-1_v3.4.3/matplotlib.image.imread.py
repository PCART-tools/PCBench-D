def imread(fname, format=None):
    """
    Read an image from a file into an array.

    Parameters
    ----------
    fname : str or file-like
        The image file to read: a filename, a URL or a file-like object opened
        in read-binary mode.

        Passing a URL is deprecated.  Please open the URL
        for reading and pass the result to Pillow, e.g. with
        ``PIL.Image.open(urllib.request.urlopen(url))``.
    format : str, optional
        The image file format assumed for reading the data. If not
        given, the format is deduced from the filename.  If nothing can
        be deduced, PNG is tried.

    Returns
    -------
    `numpy.array`
        The image data. The returned array has shape

        - (M, N) for grayscale images.
        - (M, N, 3) for RGB images.
        - (M, N, 4) for RGBA images.
    """
    # hide imports to speed initial import on systems with slow linkers
    from urllib import parse

    if format is None:
        if isinstance(fname, str):
            parsed = parse.urlparse(fname)
            # If the string is a URL (Windows paths appear as if they have a
            # length-1 scheme), assume png.
            if len(parsed.scheme) > 1:
                ext = 'png'
            else:
                ext = Path(fname).suffix.lower()[1:]
        elif hasattr(fname, 'geturl'):  # Returned by urlopen().
            # We could try to parse the url's path and use the extension, but
            # returning png is consistent with the block above.  Note that this
            # if clause has to come before checking for fname.name as
            # urlopen("file:///...") also has a name attribute (with the fixed
            # value "<urllib response>").
            ext = 'png'
        elif hasattr(fname, 'name'):
            ext = Path(fname.name).suffix.lower()[1:]
        else:
            ext = 'png'
    else:
        ext = format
    img_open = (
        PIL.PngImagePlugin.PngImageFile if ext == 'png' else PIL.Image.open)
    if isinstance(fname, str):
        parsed = parse.urlparse(fname)
        if len(parsed.scheme) > 1:  # Pillow doesn't handle URLs directly.
            _api.warn_deprecated(
                "3.4", message="Directly reading images from URLs is "
                "deprecated since %(since)s and will no longer be supported "
                "%(removal)s. Please open the URL for reading and pass the "
                "result to Pillow, e.g. with "
                "``PIL.Image.open(urllib.request.urlopen(url))``.")
            # hide imports to speed initial import on systems with slow linkers
            from urllib import request
            ssl_ctx = mpl._get_ssl_context()
            if ssl_ctx is None:
                _log.debug(
                    "Could not get certifi ssl context, https may not work."
                )
            with request.urlopen(fname, context=ssl_ctx) as response:
                import io
                try:
                    response.seek(0)
                except (AttributeError, io.UnsupportedOperation):
                    response = io.BytesIO(response.read())
                return imread(response, format=ext)
    with img_open(fname) as image:
        return (_pil_png_to_float_array(image)
                if isinstance(image, PIL.PngImagePlugin.PngImageFile) else
                pil_to_array(image))
