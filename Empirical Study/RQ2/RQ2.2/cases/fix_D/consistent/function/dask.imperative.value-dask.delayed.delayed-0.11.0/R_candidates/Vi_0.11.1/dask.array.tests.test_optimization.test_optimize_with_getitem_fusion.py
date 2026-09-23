def test_optimize_with_getitem_fusion():
    dsk = {'a': 'some-array',
           'b': (getarray, 'a', (slice(10, 20), slice(100, 200))),
           'c': (getarray, 'b', (5, slice(50, 60)))}

    result = optimize(dsk, ['c'])
    expected = {'c': (getarray, 'some-array', (15, slice(150, 160)))}
    assert result == expected
