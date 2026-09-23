def _determine_levels(index):
    """Determine the correct levels argument to groupby.
    """
    if isinstance(index, (tuple, list)) and len(index) > 1:
        return list(range(len(index)))
    else:
        return 0
