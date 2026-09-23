def test_exact_values():
    # Check that updating stored values with exact ones worked.
    for key in codata.exact_values:
        assert_((codata.exact_values[key][0] - value(key)) / value(key) == 0)
