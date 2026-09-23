@with_setup(setup_tmpdata, teardown_tmpdata)
def test_download():
    """Test that fetch_mldata is able to download and cache a data set."""

    _urlopen_ref = datasets.mldata.urlopen
    datasets.mldata.urlopen = mock_mldata_urlopen({
        'mock': {
            'label': sp.ones((150,)),
            'data': sp.ones((150, 4)),
        },
    })
    try:
        mock = fetch_mldata('mock', data_home=tmpdir)
        for n in ["COL_NAMES", "DESCR", "target", "data"]:
            assert_in(n, mock)

        assert_equal(mock.target.shape, (150,))
        assert_equal(mock.data.shape, (150, 4))

        assert_raises(datasets.mldata.HTTPError,
                      fetch_mldata, 'not_existing_name')
    finally:
        datasets.mldata.urlopen = _urlopen_ref
