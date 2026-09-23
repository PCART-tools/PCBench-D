def test_head():
    assert head((inc, 1)) == inc
    assert head((add, 1, 2)) == add
    assert head((add, (inc, 1), (inc, 1))) == add
    assert head([1, 2, 3]) == list
