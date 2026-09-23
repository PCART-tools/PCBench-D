def test_matches():
    term = (add, 2, 1)
    matches = list(rs.iter_matches(term))
    assert len(matches) == 1
    assert matches[0] == (rule1, {'a': 2})
    # Test matches specific before general
    term = (add, 1, 1)
    matches = list(rs.iter_matches(term))
    assert len(matches) == 2
    assert matches[0] == (rule1, {'a': 1})
    assert matches[1] == (rule2, {'a': 1})
    # Test matches unhashable. What it's getting rewritten to doesn't make
    # sense, this is just to test that it works. :)
    term = (add, [1], [1])
    matches = list(rs.iter_matches(term))
    assert len(matches) == 1
    assert matches[0] == (rule2, {'a': [1]})
    # Test match at depth
    term = (add, (inc, 1), (inc, 1))
    matches = list(rs.iter_matches(term))
    assert len(matches) == 3
    assert matches[0] == (rule3, {'a': 1})
    assert matches[1] == (rule4, {'a': 1, 'b': 1})
    assert matches[2] == (rule2, {'a': (inc, 1)})
    # Test non-linear pattern checking
    term = (add, 2, 3)
    matches = list(rs.iter_matches(term))
    assert len(matches) == 0
