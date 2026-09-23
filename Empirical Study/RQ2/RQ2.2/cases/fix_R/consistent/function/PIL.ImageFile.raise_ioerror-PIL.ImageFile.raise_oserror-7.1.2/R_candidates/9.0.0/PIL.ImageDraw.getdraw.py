def getdraw(im=None, hints=None):
    """
    (Experimental) A more advanced 2D drawing interface for PIL images,
    based on the WCK interface.

    :param im: The image to draw in.
    :param hints: An optional list of hints.
    :returns: A (drawing context, drawing resource factory) tuple.
    """
    # FIXME: this needs more work!
    # FIXME: come up with a better 'hints' scheme.
    handler = None
    if not hints or "nicest" in hints:
        try:
            from . import _imagingagg as handler
        except ImportError:
            pass
    if handler is None:
        from . import ImageDraw2 as handler
    if im:
        im = handler.Draw(im)
    return im, handler
