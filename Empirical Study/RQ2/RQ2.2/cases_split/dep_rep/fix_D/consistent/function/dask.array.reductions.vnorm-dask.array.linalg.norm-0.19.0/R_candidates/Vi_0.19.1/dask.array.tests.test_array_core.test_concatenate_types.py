@pytest.mark.parametrize('dtypes', [(('>f8', '>f8'), '>f8'),
                                    (('<f4', '<f8'), '<f8')])
def test_concatenate_types(dtypes):
    dts_in, dt_out = dtypes
    arrs = [np.zeros(4, dtype=dt) for dt in dts_in]
    darrs = [from_array(arr, chunks=(2,)) for arr in arrs]

    x = concatenate(darrs, axis=0)
    assert x.dtype == dt_out
