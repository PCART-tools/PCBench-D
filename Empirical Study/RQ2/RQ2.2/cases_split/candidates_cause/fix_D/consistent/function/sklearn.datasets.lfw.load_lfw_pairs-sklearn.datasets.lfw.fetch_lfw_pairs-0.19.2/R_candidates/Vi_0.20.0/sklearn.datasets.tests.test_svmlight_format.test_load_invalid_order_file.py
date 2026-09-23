def test_load_invalid_order_file():
    assert_raises(ValueError, load_svmlight_file, invalidfile2)
