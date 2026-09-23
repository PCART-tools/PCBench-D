def test_args():
    for n, cls in enumerate(classes):
        m = cls.zeros(3, 2)
        # all should give back the same type of arguments, e.g. ints for shape
        assert m.shape == (3, 2) and all(type(i) is int for i in m.shape)
        assert m.rows == 3 and type(m.rows) is int
        assert m.cols == 2 and type(m.cols) is int
        if not n % 2:
            assert type(m.flat()) in (list, tuple, Tuple)
        else:
            assert type(m.todok()) is dict
