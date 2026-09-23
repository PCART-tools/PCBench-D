def test_take():
    chunks, dsk = take('y', 'x', [(20, 20, 20, 20)], [5, 1, 47, 3], axis=0)
    expected = {('y', 0): (getitem, ('x', 0), (np.array([5, 1]),)),
                ('y', 1): (getitem, ('x', 2), (np.array([7]),)),
                ('y', 2): (getitem, ('x', 0), (np.array([3]),))}
    np.testing.assert_equal(sorted(dsk.items()), sorted(expected.items()))
    assert chunks == ((2, 1, 1),)

    chunks, dsk = take('y', 'x', [(20, 20, 20, 20), (20, 20)], [
                       5, 1, 47, 3], axis=0)
    expected = {('y', 0, 0): (getitem, ('x', 0, 0), (np.array([5, 1]), slice(None, None, None))),
                ('y', 0, 1): (getitem, ('x', 0, 1), (np.array([5, 1]), slice(None, None, None))),
                ('y', 1, 0): (getitem, ('x', 2, 0), (np.array([7]), slice(None, None, None))),
                ('y', 1, 1): (getitem, ('x', 2, 1), (np.array([7]), slice(None, None, None))),
                ('y', 2, 0): (getitem, ('x', 0, 0), (np.array([3]), slice(None, None, None))),
                ('y', 2, 1): (getitem, ('x', 0, 1), (np.array([3]), slice(None, None, None)))}
    np.testing.assert_equal(sorted(dsk.items()), sorted(expected.items()))
    assert chunks == ((2, 1, 1), (20, 20))
