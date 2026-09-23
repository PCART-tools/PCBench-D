def panel_index(time, panels, names=['time', 'panel']):
    """
    Returns a multi-index suitable for a panel-like DataFrame

    Parameters
    ----------
    time : array-like
        Time index, does not have to repeat
    panels : array-like
        Panel index, does not have to repeat
    names : list, optional
        List containing the names of the indices

    Returns
    -------
    multi_index : MultiIndex
        Time index is the first level, the panels are the second level.

    Examples
    --------
    >>> years = range(1960,1963)
    >>> panels = ['A', 'B', 'C']
    >>> panel_idx = panel_index(years, panels)
    >>> panel_idx
    MultiIndex([(1960, 'A'), (1961, 'A'), (1962, 'A'), (1960, 'B'),
                (1961, 'B'), (1962, 'B'), (1960, 'C'), (1961, 'C'),
                (1962, 'C')], dtype=object)

    or

    >>> import numpy as np
    >>> years = np.repeat(range(1960,1963), 3)
    >>> panels = np.tile(['A', 'B', 'C'], 3)
    >>> panel_idx = panel_index(years, panels)
    >>> panel_idx
    MultiIndex([(1960, 'A'), (1960, 'B'), (1960, 'C'), (1961, 'A'),
                (1961, 'B'), (1961, 'C'), (1962, 'A'), (1962, 'B'),
                (1962, 'C')], dtype=object)
    """
    time, panels = _ensure_like_indices(time, panels)
    time_factor = Categorical.from_array(time, ordered=True)
    panel_factor = Categorical.from_array(panels, ordered=True)

    labels = [time_factor.codes, panel_factor.codes]
    levels = [time_factor.categories, panel_factor.categories]
    return MultiIndex(levels, labels, sortorder=None, names=names,
                      verify_integrity=False)
