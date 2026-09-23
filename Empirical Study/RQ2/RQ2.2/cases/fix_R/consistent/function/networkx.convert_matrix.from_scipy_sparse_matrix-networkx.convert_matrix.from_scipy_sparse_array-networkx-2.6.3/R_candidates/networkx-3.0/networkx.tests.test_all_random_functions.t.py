def t(f, *args, **kwds):
    """call one function and check if global RNG changed"""
    global progress
    progress += 1
    print(progress, ",", end="")

    f(*args, **kwds)

    after_np_rv = np.random.rand()
    # if np_rv != after_np_rv:
    #    print(np_rv, after_np_rv, "don't match np!")
    assert np_rv == after_np_rv
    np.random.seed(42)

    after_py_rv = random.random()
    # if py_rv != after_py_rv:
    #    print(py_rv, after_py_rv, "don't match py!")
    assert py_rv == after_py_rv
    random.seed(42)
