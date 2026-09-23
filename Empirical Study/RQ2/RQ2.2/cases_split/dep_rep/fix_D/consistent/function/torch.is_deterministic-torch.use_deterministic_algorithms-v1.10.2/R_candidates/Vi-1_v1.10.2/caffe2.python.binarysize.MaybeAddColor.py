def MaybeAddColor(s, color):
    """Wrap the input string to the xterm green color, if color is set.
    """
    if color:
        return '\033[92m{0}\033[0m'.format(s)
    else:
        return s
