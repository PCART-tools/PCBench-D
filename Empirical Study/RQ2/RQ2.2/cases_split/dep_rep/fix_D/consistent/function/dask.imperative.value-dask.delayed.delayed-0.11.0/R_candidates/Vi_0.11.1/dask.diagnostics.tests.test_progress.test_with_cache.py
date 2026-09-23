def test_with_cache(capsys):
    cachey = pytest.importorskip('cachey')
    from dask.cache import Cache
    c = cachey.Cache(10000)
    cc = Cache(c)

    with cc:
        with ProgressBar():
            assert get({'x': (mul, 1, 2)}, 'x') == 2
    check_bar_completed(capsys)
    assert c.data['x'] == 2

    with cc:
        with ProgressBar():
            assert get({'x': (mul, 1, 2), 'y': (mul, 'x', 3)}, 'y') == 6
    check_bar_completed(capsys)
