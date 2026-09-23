@pytest.mark.parametrize("result", [None, [], ["existing"], ["existing1", "existing2"]])
@pytest.mark.parametrize("nested", [nested_depth, nested_mixed, nested_set])
def test_flatten(nested, result):
    if result is None:
        val = flatten(nested, result)
        assert len(val) == 20
    else:
        _result = copy(result)  # because pytest passes parameters as is
        nexisting = len(_result)
        val = flatten(nested, _result)
        assert len(val) == len(_result) == 20 + nexisting

    assert issubclass(type(val), tuple)
