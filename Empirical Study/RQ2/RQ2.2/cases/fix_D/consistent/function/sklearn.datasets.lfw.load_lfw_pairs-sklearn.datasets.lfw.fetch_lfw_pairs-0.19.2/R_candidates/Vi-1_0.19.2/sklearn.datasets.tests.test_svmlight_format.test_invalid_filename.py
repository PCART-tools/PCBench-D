@raises(IOError)
def test_invalid_filename():
    load_svmlight_file("trou pic nic douille")
