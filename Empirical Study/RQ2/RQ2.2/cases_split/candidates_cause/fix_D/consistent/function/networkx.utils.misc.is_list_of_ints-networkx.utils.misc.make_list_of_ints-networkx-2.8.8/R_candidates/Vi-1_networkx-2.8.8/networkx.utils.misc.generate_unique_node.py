def generate_unique_node():
    """Generate a unique node label.

    .. deprecated:: 2.6
        This is deprecated and will be removed in NetworkX v3.0.
    """
    msg = "generate_unique_node is deprecated and will be removed in 3.0. Use uuid.uuid4 instead."
    warnings.warn(msg, DeprecationWarning)
    return str(uuid.uuid4())
