def to_rgb(c):
    """Convert *c* to an RGB color, silently dropping the alpha channel."""
    return to_rgba(c)[:3]
