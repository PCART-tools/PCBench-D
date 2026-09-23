def get_undefined_blobs(ssa):
    """
    Given a ssa in the format produced by get_ssa(), return a set of blobs that
    are used before they are defined, which corresponds to inputs at version 0.
    """
    undef_blobs = set()
    for inputs, _outputs in ssa:
        undef_blobs |= set(name for (name, ver) in inputs if ver == 0)
    return undef_blobs
