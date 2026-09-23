def _get_axes(group):
    if isinstance(group, Series):
        return [group.index]
    else:
        return group.axes
