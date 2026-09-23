def test_RewriteRule():
    # Test extraneous vars are removed, varlist is correct
    assert rule1.vars == ("a",)
    assert rule1._varlist == ["a"]
    assert rule2.vars == ("a",)
    assert rule2._varlist == ["a", "a"]
    assert rule3.vars == ("a",)
    assert rule3._varlist == ["a", "a"]
    assert rule4.vars == ("a", "b")
    assert rule4._varlist == ["b", "a"]
    assert rule5.vars == ("a", "b", "c")
    assert rule5._varlist == ["c", "b", "a"]
