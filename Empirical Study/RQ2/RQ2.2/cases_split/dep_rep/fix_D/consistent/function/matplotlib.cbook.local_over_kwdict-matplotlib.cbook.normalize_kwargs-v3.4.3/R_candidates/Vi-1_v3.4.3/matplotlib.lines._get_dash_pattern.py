def _get_dash_pattern(style):
    """Convert linestyle to dash pattern."""
    # go from short hand -> full strings
    if isinstance(style, str):
        style = ls_mapper.get(style, style)
    # un-dashed styles
    if style in ['solid', 'None']:
        offset = 0
        dashes = None
    # dashed styles
    elif style in ['dashed', 'dashdot', 'dotted']:
        offset = 0
        dashes = tuple(rcParams['lines.{}_pattern'.format(style)])
    #
    elif isinstance(style, tuple):
        offset, dashes = style
        if offset is None:
            _api.warn_deprecated(
                "3.3", message="Passing the dash offset as None is deprecated "
                "since %(since)s and support for it will be removed "
                "%(removal)s; pass it as zero instead.")
            offset = 0
    else:
        raise ValueError('Unrecognized linestyle: %s' % str(style))

    # normalize offset to be positive and shorter than the dash cycle
    if dashes is not None:
        dsum = sum(dashes)
        if dsum:
            offset %= dsum

    return offset, dashes
