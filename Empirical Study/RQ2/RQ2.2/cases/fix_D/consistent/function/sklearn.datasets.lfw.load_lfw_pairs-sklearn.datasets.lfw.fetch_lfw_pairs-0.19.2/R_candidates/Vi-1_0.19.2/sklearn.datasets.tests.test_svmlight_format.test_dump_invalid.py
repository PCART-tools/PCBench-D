def test_dump_invalid():
    X, y = load_svmlight_file(datafile)

    f = BytesIO()
    y2d = [y]
    assert_raises(ValueError, dump_svmlight_file, X, y2d, f)

    f = BytesIO()
    assert_raises(ValueError, dump_svmlight_file, X, y[:-1], f)
