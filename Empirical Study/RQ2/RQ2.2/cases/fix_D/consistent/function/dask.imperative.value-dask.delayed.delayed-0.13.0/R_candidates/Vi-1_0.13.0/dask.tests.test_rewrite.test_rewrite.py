def test_rewrite():
    # Rewrite inside list
    term = (sum, [(add, 1, 1), (add, 1, 1), (add, 1, 1)])
    new_term = rs.rewrite(term)
    assert new_term == (add, (add, (inc, 1), (inc, 1)), (inc, 1))
    # Rules aren't applied to exhaustion, this can be further simplified
    new_term = rs.rewrite(new_term)
    assert new_term == (add, (add, (double, 1), 2), (inc, 1))
    term = (add, (add, (add, (add, 1, 2), (add, 1, 2)), (add, (add, 1, 2), (add, 1, 2))), 1)
    assert rs.rewrite(term) == (inc, (double, (double, (add, 1, 2))))
    # Callable RewriteRule rhs
    term = (list, [1, 2, 3])
    assert rs.rewrite(term) == [1, 2, 3]
    term = (list, (map, inc, [1, 2, 3]))
    assert rs.rewrite(term) == term
