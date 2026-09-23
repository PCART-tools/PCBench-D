@pytest.mark.parametrize("data", [
    ["1,2\n", "2,3\r\n"],  # a universal newline
    ["1,2\n", "'2\n',3\n"],  # a quoted newline
    ["1,2\n", "'2\r',3\n"],
    ["1,2\n", "'2\r\n',3\n"],
])
def test_good_newline_in_iterator(data):
    # The quoted newlines will be untransformed here, but are just whitespace.
    res = np.loadtxt(data, delimiter=",", quotechar="'")
    assert_array_equal(res, [[1., 2.], [2., 3.]])
