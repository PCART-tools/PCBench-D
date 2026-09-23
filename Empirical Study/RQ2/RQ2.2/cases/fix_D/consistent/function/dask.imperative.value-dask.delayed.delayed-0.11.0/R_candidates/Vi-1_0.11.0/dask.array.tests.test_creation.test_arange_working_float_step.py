def test_arange_working_float_step():
    """Sometimes floating point step arguments work, but this could be platform
    dependent.
    """
    darr = da.arange(3.3, -9.1, -.25, chunks=3)
    nparr = np.arange(3.3, -9.1, -.25)
    eq(darr, nparr)
