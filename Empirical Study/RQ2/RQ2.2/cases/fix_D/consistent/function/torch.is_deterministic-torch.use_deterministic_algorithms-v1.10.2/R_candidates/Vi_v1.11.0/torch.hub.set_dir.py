def set_dir(d):
    r"""
    Optionally set the Torch Hub directory used to save downloaded models & weights.

    Args:
        d (string): path to a local folder to save downloaded models & weights.
    """
    global _hub_dir
    _hub_dir = d
