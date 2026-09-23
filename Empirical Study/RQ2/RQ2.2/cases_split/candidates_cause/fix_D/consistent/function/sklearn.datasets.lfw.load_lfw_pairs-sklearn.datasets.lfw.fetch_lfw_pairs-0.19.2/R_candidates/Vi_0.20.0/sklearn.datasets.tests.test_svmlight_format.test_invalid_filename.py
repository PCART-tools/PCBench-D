def test_invalid_filename():
    assert_raises(IOError, load_svmlight_file, "trou pic nic douille")
