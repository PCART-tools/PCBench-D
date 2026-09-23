def test_two_gets():
    with prof:
        get(dsk, 'e')
    n = len(prof.results)

    dsk2 = {'x': (add, 1, 2), 'y': (add, 'x', 'x')}

    with prof:
        get(dsk2, 'y')
    m = len(prof.results)

    with prof:
        get(dsk, 'e')
        get(dsk2, 'y')
        get(dsk, 'e')

    assert len(prof.results) == n + m + n
