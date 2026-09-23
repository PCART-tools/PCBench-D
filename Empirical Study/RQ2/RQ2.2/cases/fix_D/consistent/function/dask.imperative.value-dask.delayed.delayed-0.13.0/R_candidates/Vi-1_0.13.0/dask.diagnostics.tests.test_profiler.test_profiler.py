def test_profiler():
    with prof:
        out = get(dsk, 'e')
    assert out == 6
    prof_data = sorted(prof.results, key=lambda d: d.key)
    keys = [i.key for i in prof_data]
    assert keys == ['c', 'd', 'e']
    tasks = [i.task for i in prof_data]
    assert tasks == [(add, 'a', 'b'), (mul, 'a', 'b'), (mul, 'c', 'd')]
    prof.clear()
    assert prof.results == []
