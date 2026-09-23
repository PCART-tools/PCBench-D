def test_format_time():
    assert format_time(1.4) == ' 1.4s'
    assert format_time(10.4) == '10.4s'
    assert format_time(100.4) == ' 1min 40.4s'
    assert format_time(1000.4) == '16min 40.4s'
    assert format_time(10000.4) == ' 2hr 46min 40.4s'
