def _devicePixelRatioF(obj):
    """
    Return obj.devicePixelRatioF() with graceful fallback for older Qt.

    This can be replaced by the direct call when we require Qt>=5.6.
    """
    try:
        # Not available on Qt<5.6
        return obj.devicePixelRatioF() or 1
    except AttributeError:
        pass
    try:
        # Not available on Qt4 or some older Qt5.
        # self.devicePixelRatio() returns 0 in rare cases
        return obj.devicePixelRatio() or 1
    except AttributeError:
        return 1
