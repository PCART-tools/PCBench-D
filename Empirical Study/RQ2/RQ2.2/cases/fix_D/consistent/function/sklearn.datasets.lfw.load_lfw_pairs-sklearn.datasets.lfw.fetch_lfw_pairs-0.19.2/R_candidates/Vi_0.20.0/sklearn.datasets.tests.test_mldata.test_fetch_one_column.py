@pytest.mark.filterwarnings('ignore::DeprecationWarning')
def test_fetch_one_column(tmpdata):
    _urlopen_ref = datasets.mldata.urlopen
    try:
        dataname = 'onecol'
        # create fake data set in cache
        x = sp.arange(6).reshape(2, 3)
        datasets.mldata.urlopen = mock_mldata_urlopen({dataname: {'x': x}})

        dset = fetch_mldata(dataname, data_home=tmpdata)
        for n in ["COL_NAMES", "DESCR", "data"]:
            assert_in(n, dset)
        assert_not_in("target", dset)

        assert_equal(dset.data.shape, (2, 3))
        assert_array_equal(dset.data, x)

        # transposing the data array
        dset = fetch_mldata(dataname, transpose_data=False, data_home=tmpdata)
        assert_equal(dset.data.shape, (3, 2))
    finally:
        datasets.mldata.urlopen = _urlopen_ref
