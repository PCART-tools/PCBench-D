def _normalize_namescope(namescope):
    if namescope and namescope[-1] != scope._NAMESCOPE_SEPARATOR:
        return namescope + scope._NAMESCOPE_SEPARATOR
    else:
        return namescope
