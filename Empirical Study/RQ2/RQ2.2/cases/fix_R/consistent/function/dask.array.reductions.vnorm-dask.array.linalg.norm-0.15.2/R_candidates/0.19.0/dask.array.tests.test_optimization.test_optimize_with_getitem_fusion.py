def test_optimize_with_getitem_fusion():
    dsk = {'a': 'some-array',
           'b': (getter, 'a', (slice(10, 20), slice(100, 200))),
           'c': (getter, 'b', (5, slice(50, 60)))}

    result = optimize(dsk, ['c'])
    expected_task = (getter, 'some-array', (15, slice(150, 160)))
    assert any(v == expected_task for v in result.values())
    assert len(result) < len(dsk)
