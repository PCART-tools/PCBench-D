def generate_bins_generic(values, binner, closed):
    """
    Generate bin edge offsets and bin labels for one array using another array
    which has bin edge values. Both arrays must be sorted.

    Parameters
    ----------
    values : array of values
    binner : a comparable array of values representing bins into which to bin
        the first array. Note, 'values' end-points must fall within 'binner'
        end-points.
    closed : which end of bin is closed; left (default), right

    Returns
    -------
    bins : array of offsets (into 'values' argument) of bins.
        Zero and last edge are excluded in result, so for instance the first
        bin is values[0:bin[0]] and the last is values[bin[-1]:]
    """
    lenidx = len(values)
    lenbin = len(binner)

    if lenidx <= 0 or lenbin <= 0:
        raise ValueError("Invalid length for values or for binner")

    # check binner fits data
    if values[0] < binner[0]:
        raise ValueError("Values falls before first bin")

    if values[lenidx - 1] > binner[lenbin - 1]:
        raise ValueError("Values falls after last bin")

    bins = np.empty(lenbin - 1, dtype=np.int64)

    j = 0  # index into values
    bc = 0  # bin count

    # linear scan, presume nothing about values/binner except that it fits ok
    for i in range(0, lenbin - 1):
        r_bin = binner[i + 1]

        # count values in current bin, advance to next bin
        while j < lenidx and (values[j] < r_bin or
                              (closed == 'right' and values[j] == r_bin)):
            j += 1

        bins[bc] = j
        bc += 1

    return bins
