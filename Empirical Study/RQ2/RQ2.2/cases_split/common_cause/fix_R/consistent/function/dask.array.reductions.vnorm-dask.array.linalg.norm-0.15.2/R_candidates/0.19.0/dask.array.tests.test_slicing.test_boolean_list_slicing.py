@pytest.mark.skipif(np.__version__ < '1.13.0',
                    reason='boolean lists are not treated as boolean indexes')
def test_boolean_list_slicing():
    with pytest.raises(IndexError):
        da.asarray(range(2))[[True]]
    with pytest.raises(IndexError):
        da.asarray(range(2))[[False, False, False]]
    x = np.arange(5)
    ind = [True, False, False, False, True]
    assert_eq(da.asarray(x)[ind], x[ind])
    # https://github.com/dask/dask/issues/3706
    ind = [True]
    assert_eq(da.asarray([0])[ind], np.arange(1)[ind])
