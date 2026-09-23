def test_dict_to_numpy_array_deprecations():
    np = pytest.importorskip("numpy")
    d = {"a": 1}
    with pytest.deprecated_call():
        nx.utils.dict_to_numpy_array1(d)
    d2 = {"a": {"b": 2}}
    with pytest.deprecated_call():
        nx.utils.dict_to_numpy_array2(d2)
