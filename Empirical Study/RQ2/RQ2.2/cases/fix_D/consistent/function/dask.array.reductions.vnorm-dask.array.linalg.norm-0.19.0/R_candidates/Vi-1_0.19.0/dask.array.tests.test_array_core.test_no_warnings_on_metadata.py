def test_no_warnings_on_metadata():
    x = da.ones(5, chunks=3)
    with warnings.catch_warnings(record=True) as record:
        da.arccos(x)

    assert not record
