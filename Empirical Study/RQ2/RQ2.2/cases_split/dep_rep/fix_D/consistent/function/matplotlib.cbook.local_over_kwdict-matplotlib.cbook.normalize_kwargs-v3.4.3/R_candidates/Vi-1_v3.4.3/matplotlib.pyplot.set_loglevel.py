@functools.wraps(matplotlib.set_loglevel)
def set_loglevel(*args, **kwargs):  # Ensure this appears in the pyplot docs.
    return matplotlib.set_loglevel(*args, **kwargs)
