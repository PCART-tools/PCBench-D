@_api.deprecated("3.5", alternative="mdates.num2date(e).timestamp()")
def num2epoch(d):
    """
    Convert days since Matplotlib epoch to UNIX time.

    Parameters
    ----------
    d : list of floats
        Time in days since Matplotlib epoch (see `~.dates.get_epoch()`).

    Returns
    -------
    `numpy.array`
        Time in seconds since 1970-01-01.
    """
    dt = (np.datetime64('1970-01-01T00:00:00', 's') -
          np.datetime64(get_epoch(), 's')).astype(float)

    return np.asarray(d) * SEC_PER_DAY - dt
