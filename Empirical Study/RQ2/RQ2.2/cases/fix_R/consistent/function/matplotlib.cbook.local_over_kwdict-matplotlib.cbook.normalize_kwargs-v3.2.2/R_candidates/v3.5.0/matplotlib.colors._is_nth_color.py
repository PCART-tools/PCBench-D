def _is_nth_color(c):
    """Return whether *c* can be interpreted as an item in the color cycle."""
    return isinstance(c, str) and re.match(r"\AC[0-9]+\Z", c)
