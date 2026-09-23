@pytest.mark.xfail(reason="Casting floats to ints is not supported since edge"
                          "behavior is not specified or guaranteed by NumPy.")
def test_arange_cast_float_int_step():
    darr = da.arange(3.3, -9.1, -.25, chunks=3, dtype='i8')
    nparr = np.arange(3.3, -9.1, -.25, dtype='i8')
    eq(darr, nparr)
