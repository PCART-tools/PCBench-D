def _convert_grouper(axis, grouper):
    if isinstance(grouper, dict):
        return grouper.get
    elif isinstance(grouper, Series):
        if grouper.index.equals(axis):
            return grouper._values
        else:
            return grouper.reindex(axis)._values
    elif isinstance(grouper, (list, Series, Index, np.ndarray)):
        if len(grouper) != len(axis):
            raise AssertionError('Grouper and axis must be same length')
        return grouper
    else:
        return grouper
