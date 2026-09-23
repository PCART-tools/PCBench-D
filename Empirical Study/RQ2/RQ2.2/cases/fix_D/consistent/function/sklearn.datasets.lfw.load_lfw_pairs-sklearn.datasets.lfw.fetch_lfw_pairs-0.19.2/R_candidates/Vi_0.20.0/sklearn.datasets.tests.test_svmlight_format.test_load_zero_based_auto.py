def test_load_zero_based_auto():
    data1 = b("-1 1:1 2:2 3:3\n")
    data2 = b("-1 0:0 1:1\n")

    f1 = BytesIO(data1)
    X, y = load_svmlight_file(f1, zero_based="auto")
    assert_equal(X.shape, (1, 3))

    f1 = BytesIO(data1)
    f2 = BytesIO(data2)
    X1, y1, X2, y2 = load_svmlight_files([f1, f2], zero_based="auto")
    assert_equal(X1.shape, (1, 4))
    assert_equal(X2.shape, (1, 4))
