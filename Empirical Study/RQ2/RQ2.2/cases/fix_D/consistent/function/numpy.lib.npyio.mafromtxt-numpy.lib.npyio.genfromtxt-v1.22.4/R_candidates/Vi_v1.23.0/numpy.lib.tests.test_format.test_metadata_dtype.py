@pytest.mark.parametrize('dt, fail', [
    (np.dtype({'names': ['a', 'b'], 'formats':  [float, np.dtype('S3',
                 metadata={'some': 'stuff'})]}), True),
    (np.dtype(int, metadata={'some': 'stuff'}), False),
    (np.dtype([('subarray', (int, (2,)))], metadata={'some': 'stuff'}), False),
    # recursive: metadata on the field of a dtype
    (np.dtype({'names': ['a', 'b'], 'formats': [
        float, np.dtype({'names': ['c'], 'formats': [np.dtype(int, metadata={})]})
    ]}), False)
    ])
@pytest.mark.skipif(IS_PYPY and sys.implementation.version <= (7, 3, 8),
        reason="PyPy bug in error formatting")
def test_metadata_dtype(dt, fail):
    # gh-14142
    arr = np.ones(10, dtype=dt)
    buf = BytesIO()
    with assert_warns(UserWarning):
        np.save(buf, arr)
    buf.seek(0)
    if fail:
        with assert_raises(ValueError):
            np.load(buf)
    else:
        arr2 = np.load(buf)
        # BUG: assert_array_equal does not check metadata
        from numpy.lib.format import _has_metadata
        assert_array_equal(arr, arr2)
        assert _has_metadata(arr.dtype)
        assert not _has_metadata(arr2.dtype)
