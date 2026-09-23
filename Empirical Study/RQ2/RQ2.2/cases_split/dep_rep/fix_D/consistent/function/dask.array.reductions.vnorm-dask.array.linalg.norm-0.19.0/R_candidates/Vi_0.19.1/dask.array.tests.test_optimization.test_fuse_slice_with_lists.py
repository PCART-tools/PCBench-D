def test_fuse_slice_with_lists():
    assert fuse_slice(slice(10, 20, 2), [1, 2, 3]) == [12, 14, 16]
    assert fuse_slice([10, 20, 30, 40, 50], [3, 1, 2]) == [40, 20, 30]
    assert fuse_slice([10, 20, 30, 40, 50], 3) == 40
    assert fuse_slice([10, 20, 30, 40, 50], -1) == 50
    assert fuse_slice([10, 20, 30, 40, 50], slice(1, None, 2)) == [20, 40]
    assert fuse_slice((slice(None), slice(0, 10), [1, 2, 3]),
                      (slice(None), slice(1, 5), slice(None))) == (slice(0, None), slice(1, 5), [1, 2, 3])
    assert fuse_slice((slice(None), slice(None), [1, 2, 3]),
                      (slice(None), slice(1, 5), 1)) == (slice(0, None), slice(1, 5), 2)
