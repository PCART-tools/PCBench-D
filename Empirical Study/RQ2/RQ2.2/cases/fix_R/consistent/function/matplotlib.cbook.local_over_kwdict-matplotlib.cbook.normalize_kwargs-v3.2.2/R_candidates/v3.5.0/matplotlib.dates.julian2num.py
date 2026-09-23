def julian2num(j):
    """
    Convert a Julian date (or sequence) to a Matplotlib date (or sequence).

    Parameters
    ----------
    j : float or sequence of floats
        Julian dates (days relative to 4713 BC Jan 1, 12:00:00 Julian
        calendar or 4714 BC Nov 24, 12:00:00, proleptic Gregorian calendar).

    Returns
    -------
    float or sequence of floats
        Matplotlib dates (days relative to `.get_epoch`).
    """
    ep = np.datetime64(get_epoch(), 'h').astype(float) / 24.
    ep0 = np.datetime64('0000-12-31T00:00:00', 'h').astype(float) / 24.
    # Julian offset defined above is relative to 0000-12-31, but we need
    # relative to our current epoch:
    dt = JULIAN_OFFSET - ep0 + ep
    return np.subtract(j, dt)  # Handles both scalar & nonscalar j.
