def test_basic():
    s = Store()
    s['x'] = 1
    s['y'] = (inc, 'x')
    s['z'] = (add, 'x', 'y')

    assert s.data == set(['x'])

    assert s['z'] == 3
    assert 'x' in s.data
    assert s.cache['z'] == 3
    assert s.cache['y'] == 2

    assert len(s.access_times['z']) == 1
    assert len(s.access_times['y']) == 1
    assert len(s.access_times['x']) == 2
    assert s.compute_time['z'] < 0.1

    cache = s.cache.copy()
    assert s['z'] == 3
    assert s.cache == cache
    assert len(s.access_times['z']) == 2
    assert len(s.access_times['y']) == 1
    assert len(s.access_times['x']) == 2

    assert s[5] == 5
    assert list(s[['x', 'y']]) == [s['x'], s['y']]

    def reassign():
        s['x'] = 2
    assert raises(Exception, reassign)
