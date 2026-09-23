@pytest.mark.parametrize("x, tdelta",
                         [(1, datetime.timedelta(days=1)),
                          ([1, 1.5], [datetime.timedelta(days=1),
                                      datetime.timedelta(days=1.5)])])
def test_num2timedelta(x, tdelta):
    dt = mdates.num2timedelta(x)
    assert dt == tdelta
