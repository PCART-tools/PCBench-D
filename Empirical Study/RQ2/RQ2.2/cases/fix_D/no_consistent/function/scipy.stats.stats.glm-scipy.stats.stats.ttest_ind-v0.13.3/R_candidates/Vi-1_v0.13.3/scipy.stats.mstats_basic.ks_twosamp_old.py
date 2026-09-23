def ks_twosamp_old(data1, data2):
    """ Computes the Kolmogorov-Smirnov statistic on 2 samples.

    Returns
    -------
    KS D-value, p-value

    """
    (data1, data2) = [ma.asarray(d).compressed() for d in (data1,data2)]
    return stats.ks_2samp(data1,data2)
