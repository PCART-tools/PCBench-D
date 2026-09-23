def test_fuse_slices_with_alias():
    dsk = {'x': np.arange(16).reshape((4, 4)),
           ('dx', 0, 0): (getter, 'x', (slice(0, 4), slice(0, 4))),
           ('alias', 0, 0): ('dx', 0, 0),
           ('dx2', 0): (getitem, ('alias', 0, 0), (slice(None), 0))}
    keys = [('dx2', 0)]
    dsk2 = optimize(dsk, keys)
    assert len(dsk2) == 3
    fused_key = set(dsk2).difference(['x', ('dx2', 0)]).pop()
    assert dsk2[fused_key] == (getter, 'x', (slice(0, 4), 0))
