@pytest.mark.parametrize('skiprows', [0, 1, 2, 3])
def test_structured_dtype_and_skiprows_no_empty_lines(
        skiprows, mixed_types_structured):
    data, dtype, expected = mixed_types_structured
    a = np.loadtxt(data, dtype=dtype, delimiter=";", skiprows=skiprows)
    assert_array_equal(a, expected[skiprows:])
