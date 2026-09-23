def test_load_zero_based():
    f = BytesIO(b("-1 4:1.\n1 0:1\n"))
    assert_raises(ValueError, load_svmlight_file, f, zero_based=False)
