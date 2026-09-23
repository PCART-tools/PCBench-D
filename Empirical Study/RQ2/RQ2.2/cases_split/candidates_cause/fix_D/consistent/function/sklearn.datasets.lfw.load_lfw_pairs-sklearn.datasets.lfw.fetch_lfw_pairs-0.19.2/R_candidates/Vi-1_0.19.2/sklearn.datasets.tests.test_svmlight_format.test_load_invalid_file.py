@raises(ValueError)
def test_load_invalid_file():
    load_svmlight_file(invalidfile)
