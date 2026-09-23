@_api.deprecated("3.5",
                 alternative="mdates.date2num(datetime.utcfromtimestamp(e))")
def epoch2num(e):
    """
    Convert UNIX time to days since Matplotlib epoch.

    Parameters
    ----------
    e : list of floats
        Time in seconds since 1970-01-01.

    Returns
    -------
    `numpy.array`
        Time in days since Matplotlib epoch (see `~.dates.get_epoch()`).
    """

    dt = (np.datetime64('1970-01-01T00:00:00', 's') -
          np.datetime64(get_epoch(), 's')).astype(float)

    return (dt + np.asarray(e)) / SEC_PER_DAY
