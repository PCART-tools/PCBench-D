def test_args():
    assert args((inc, 1)) == (1,)
    assert args((add, 1, 2)) == (1, 2)
    assert args(1) == ()
    assert args([1, 2, 3]) == [1, 2, 3]
