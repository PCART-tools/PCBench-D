def make_axis_dummies(frame, axis='minor', transform=None):
    """
    Construct 1-0 dummy variables corresponding to designated axis
    labels

    Parameters
    ----------
    frame : DataFrame
    axis : {'major', 'minor'}, default 'minor'
    transform : function, default None
        Function to apply to axis labels first. For example, to
        get "day of week" dummies in a time series regression
        you might call::

            make_axis_dummies(panel, axis='major',
                              transform=lambda d: d.weekday())
    Returns
    -------
    dummies : DataFrame
        Column names taken from chosen axis
    """
    numbers = {'major': 0, 'minor': 1}
    num = numbers.get(axis, axis)

    items = frame.index.levels[num]
    labels = frame.index.labels[num]
    if transform is not None:
        mapped_items = items.map(transform)
        cat = Categorical.from_array(mapped_items.take(labels), ordered=True)
        labels = cat.codes
        items = cat.categories

    values = np.eye(len(items), dtype=float)
    values = values.take(labels, axis=0)

    return DataFrame(values, columns=items, index=frame.index)
