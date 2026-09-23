@pytest.mark.xfail(reason="arange with a floating point step value can fail"
                          "due to numerical instability.")
def test_arange_float_step():
    darr = da.arange(2., 13., .3, chunks=4)
    nparr = np.arange(2., 13., .3)
    eq(darr, nparr)

    darr = da.arange(7.7, 1.5, -.8, chunks=3)
    nparr = np.arange(7.7, 1.5, -.8)
    eq(darr, nparr)
