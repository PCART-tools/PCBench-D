def get_epoch():
    """
    Get the epoch used by `.dates`.

    Returns
    -------
    epoch : str
        String for the epoch (parsable by `numpy.datetime64`).
    """
    global _epoch

    if _epoch is None:
        _epoch = mpl.rcParams['date.epoch']
    return _epoch
