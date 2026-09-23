def register(viewer, order=1):
    """
    The :py:func:`register` function is used to register additional viewers.

    :param viewer: The viewer to be registered.
    :param order:
        Zero or a negative integer to prepend this viewer to the list,
        a positive integer to append it.
    """
    try:
        if issubclass(viewer, Viewer):
            viewer = viewer()
    except TypeError:
        pass  # raised if viewer wasn't a class
    if order > 0:
        _viewers.append(viewer)
    else:
        _viewers.insert(0, viewer)
