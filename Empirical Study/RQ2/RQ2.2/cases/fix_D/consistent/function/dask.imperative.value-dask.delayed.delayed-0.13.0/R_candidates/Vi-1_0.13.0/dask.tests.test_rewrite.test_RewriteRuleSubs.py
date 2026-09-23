def test_RewriteRuleSubs():
    # Test both rhs substitution and callable rhs
    assert rule1.subs({'a': 1}) == (inc, 1)
    assert rule6.subs({'x': [1, 2, 3]}) == [1, 2, 3]
