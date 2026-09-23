@pytest.mark.parametrize("data", [
    ["1,2\n", "2\n,3\n"],
    ["1,2\n", "2\r,3\n"]])
def test_bad_newline_in_iterator(data):
    # In NumPy <=1.22 this was accepted, because newlines were completely
    # ignored when the input was an iterable.  This could be changed, but right
    # now, we raise an error.
    msg = "Found an unquoted embedded newline within a single line"
    with pytest.raises(ValueError, match=msg):
        np.loadtxt(data, delimiter=",")
