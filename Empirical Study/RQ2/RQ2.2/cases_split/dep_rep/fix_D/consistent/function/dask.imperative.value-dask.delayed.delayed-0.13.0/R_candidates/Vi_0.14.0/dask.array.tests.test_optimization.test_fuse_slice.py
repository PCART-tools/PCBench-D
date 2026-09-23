def test_fuse_slice():
    assert fuse_slice(slice(10, 15), slice(0, 5, 2)) == slice(10, 15, 2)

    assert (fuse_slice((slice(100, 200),), (None, slice(10, 20))) ==
            (None, slice(110, 120)))
    assert (fuse_slice((slice(100, 200),), (slice(10, 20), None)) ==
            (slice(110, 120), None))
    assert (fuse_slice((1,), (None,)) ==
            (1, None))
    assert (fuse_slice((1, slice(10, 20)), (None, None, 3, None)) ==
            (1, None, None, 13, None))

    with pytest.raises(NotImplementedError):
        fuse_slice(slice(10, 15, 2), -1)
