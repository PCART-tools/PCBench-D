def test_pickle_globals():
    """ For the function f(x) defined below, the only globals added in pickling
    should be 'np' and '__builtins__'"""
    def f(x):
        return np.sin(x) + np.cos(x)

    assert set(['np', '__builtins__']) == set(
        _loads(_dumps(f)).__globals__.keys())
