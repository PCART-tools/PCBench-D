def NeedAll(op, g_output):
    """A sanity check to make sure that all the gradient are given."""
    for name, g in zip(op.output, g_output):
        if g is None:
            raise RuntimeError(
                'Need gradient for "%s" but it is not provided.' % name)
    return g_output
