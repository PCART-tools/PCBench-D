def test_frompyfunc_wrapper():
    f = da_frompyfunc(add, 2, 1)
    np_f = np.frompyfunc(add, 2, 1)
    x = np.array([1, 2, 3])

    # Callable
    np.testing.assert_equal(f(x, 1), np_f(x, 1))

    # picklable
    f2 = pickle.loads(pickle.dumps(f))
    np.testing.assert_equal(f2(x, 1), np_f(x, 1))

    # Attributes
    assert f.ntypes == np_f.ntypes
    with pytest.raises(AttributeError):
        f.not_an_attribute

    # Tab completion
    assert 'ntypes' in dir(f)

    # Methods
    np.testing.assert_equal(f.outer(x, x), np_f.outer(x, x))

    # funcname
    assert f.__name__ == 'frompyfunc-add'

    # repr
    assert repr(f) == "da.frompyfunc<add, 2, 1>"

    # tokenize
    assert (tokenize(da_frompyfunc(add, 2, 1)) ==
            tokenize(da_frompyfunc(add, 2, 1)))
