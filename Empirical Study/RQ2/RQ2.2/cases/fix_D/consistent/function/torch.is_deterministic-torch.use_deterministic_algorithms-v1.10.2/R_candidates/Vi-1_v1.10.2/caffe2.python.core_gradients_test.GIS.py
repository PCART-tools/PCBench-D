def GIS(op):
    """A test util function to generate the gradient name for input."""
    return [s + '_grad' for s in op.input]
