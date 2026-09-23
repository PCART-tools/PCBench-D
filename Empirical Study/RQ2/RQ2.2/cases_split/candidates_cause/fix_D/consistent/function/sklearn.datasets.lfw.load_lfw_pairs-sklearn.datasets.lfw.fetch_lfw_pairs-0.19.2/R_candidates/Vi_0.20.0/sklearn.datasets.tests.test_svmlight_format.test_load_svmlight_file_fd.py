def test_load_svmlight_file_fd():
    # test loading from file descriptor
    X1, y1 = load_svmlight_file(datafile)

    fd = os.open(datafile, os.O_RDONLY)
    try:
        X2, y2 = load_svmlight_file(fd)
        assert_array_almost_equal(X1.data, X2.data)
        assert_array_almost_equal(y1, y2)
    finally:
        os.close(fd)
