def test_fetch():
    try:
        data = fetch()
    except IOError:
        raise SkipTest("California housing dataset can not be loaded.")
    assert((20640, 8) == data.data.shape)
    assert((20640, ) == data.target.shape)

    # test return_X_y option
    fetch_func = partial(fetch)
    check_return_X_y(data, fetch_func)
