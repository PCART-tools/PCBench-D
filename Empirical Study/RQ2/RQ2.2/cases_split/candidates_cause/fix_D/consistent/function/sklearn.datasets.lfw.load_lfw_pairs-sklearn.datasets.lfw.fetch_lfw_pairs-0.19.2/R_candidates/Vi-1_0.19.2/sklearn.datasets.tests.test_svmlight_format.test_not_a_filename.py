@raises(TypeError)
def test_not_a_filename():
    # in python 3 integers are valid file opening arguments (taken as unix
    # file descriptors)
    load_svmlight_file(.42)
