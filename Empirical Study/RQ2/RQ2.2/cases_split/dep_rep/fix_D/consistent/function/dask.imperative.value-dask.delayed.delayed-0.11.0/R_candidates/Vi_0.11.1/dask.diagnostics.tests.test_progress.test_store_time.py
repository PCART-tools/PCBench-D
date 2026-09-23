def test_store_time():
    p = ProgressBar()
    with p:
        get({'x': 1}, 'x')

    assert isinstance(p.last_duration, float)
