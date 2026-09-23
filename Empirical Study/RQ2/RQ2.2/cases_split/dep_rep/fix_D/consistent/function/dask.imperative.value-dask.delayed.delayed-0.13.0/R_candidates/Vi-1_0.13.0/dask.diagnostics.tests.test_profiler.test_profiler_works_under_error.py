def test_profiler_works_under_error():
    div = lambda x, y: x / y
    dsk = {'x': (div, 1, 1), 'y': (div, 'x', 2), 'z': (div, 'y', 0)}

    with ignoring(ZeroDivisionError):
        with prof:
            get(dsk, 'z')

    assert all(len(v) == 5 for v in prof.results)
    assert len(prof.results) == 2
