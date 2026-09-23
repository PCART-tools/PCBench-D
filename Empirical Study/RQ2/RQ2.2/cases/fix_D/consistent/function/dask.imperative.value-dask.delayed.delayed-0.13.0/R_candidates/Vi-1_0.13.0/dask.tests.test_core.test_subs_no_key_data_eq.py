def test_subs_no_key_data_eq():
    # Numpy throws a deprecation warning on bool(array == scalar), which
    # pollutes the terminal. This test checks that `subs` never tries to
    # compare keys (scalars) with values (which could be arrays)`subs` never
    # tries to compare keys (scalars) with values (which could be arrays).
    a = MutateOnEq()
    subs(a, 'x', 1)
    assert a.hit_eq == 0
    subs((add, a, 'x'), 'x', 1)
    assert a.hit_eq == 0
