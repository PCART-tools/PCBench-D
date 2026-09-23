def assert_dicts_equal(dict_0, dict_1):
    """Builtin dict comparison will not compare numpy arrays.
    e.g.
        x = {"a": np.ones((2, 1))}
        x == x  # Raises ValueError
    """
    assert set(dict_0.keys()) == set(dict_0.keys())
    assert all(np.all(v == dict_1[k]) for k, v in dict_0.items() if k != "dtype")
