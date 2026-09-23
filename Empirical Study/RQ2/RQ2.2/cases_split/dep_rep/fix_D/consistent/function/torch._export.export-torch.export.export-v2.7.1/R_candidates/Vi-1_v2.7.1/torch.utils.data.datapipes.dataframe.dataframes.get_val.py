def get_val(capture):
    if isinstance(capture, Capture):
        return capture.execute()
    elif isinstance(capture, str):
        return f'"{capture}"'
    else:
        return capture
