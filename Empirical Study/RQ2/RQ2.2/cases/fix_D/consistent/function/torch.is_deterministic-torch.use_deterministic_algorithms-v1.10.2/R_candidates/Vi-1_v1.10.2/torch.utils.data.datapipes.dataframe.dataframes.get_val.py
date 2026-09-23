def get_val(capture):
    if isinstance(capture, Capture):
        return capture.execute()
    elif isinstance(capture, str):
        return '"%s"' % capture
    else:
        return capture
