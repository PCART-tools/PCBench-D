def rsh(data, points=None):
    """
    Evaluates Rosenblatt's shifted histogram estimators for each point
    on the dataset 'data'.

    Parameters
    ----------
    data : sequence
        Input data. Masked values are ignored.
    points : sequence
        Sequence of points where to evaluate Rosenblatt shifted histogram.
        If None, use the data.

    """
    data = ma.array(data, copy=False)
    if points is None:
        points = data
    else:
        points = np.array(points, copy=False, ndmin=1)

    if data.ndim != 1:
        raise AttributeError("The input array should be 1D only !")

    n = data.count()
    r = idealfourths(data, axis=None)
    h = 1.2 * (r[-1]-r[0]) / n**(1./5)
    nhi = (data[:,None] <= points[None,:] + h).sum(0)
    nlo = (data[:,None] < points[None,:] - h).sum(0)
    return (nhi-nlo) / (2.*n*h)
