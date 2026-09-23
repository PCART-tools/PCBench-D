def _offset(window, center):
    if not com.is_integer(window):
        window = len(window)
    offset = (window - 1) / 2. if center else 0
    try:
        return int(offset)
    except:
        return offset.astype(int)
