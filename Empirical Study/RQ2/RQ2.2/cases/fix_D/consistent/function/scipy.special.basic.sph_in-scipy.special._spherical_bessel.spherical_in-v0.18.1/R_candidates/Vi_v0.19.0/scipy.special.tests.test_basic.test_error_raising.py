@with_special_errors
def test_error_raising():
    assert_raises(special.SpecialFunctionError, special.iv, 1, 1e99j)
