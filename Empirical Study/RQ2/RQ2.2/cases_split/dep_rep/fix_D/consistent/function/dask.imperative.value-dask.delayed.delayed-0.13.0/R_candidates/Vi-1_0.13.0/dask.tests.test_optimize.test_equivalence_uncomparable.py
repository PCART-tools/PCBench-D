def test_equivalence_uncomparable():
    t1 = Uncomparable()
    t2 = Uncomparable()
    pytest.raises(TypeError, lambda: t1 == t2)
    assert equivalent(t1, t1)
    assert not equivalent(t1, t2)
    assert equivalent((add, t1, 0), (add, t1, 0))
    assert not equivalent((add, t1, 0), (add, t2, 0))
