@pytest.mark.skipif(sys.flags.optimize == 2, reason="-OO discards docstrings")
def test_deprecate_preserve_whitespace():
    assert_('\n        Bizarre' in new_func5.__doc__)
