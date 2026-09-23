def _is_transparent(rgb_or_rgba):
    if rgb_or_rgba is None:
        return True  # Consistent with rgbFace semantics.
    elif len(rgb_or_rgba) == 4:
        if rgb_or_rgba[3] == 0:
            return True
        if rgb_or_rgba[3] != 1:
            _log.warning(
                "The PostScript backend does not support transparency; "
                "partially transparent artists will be rendered opaque.")
        return False
    else:  # len() == 3.
        return False
