def test_context_with_badparam():
    original_value = 'gray'
    other_value = 'blue'
    d = OrderedDict([(PARAM, original_value), ('badparam', None)])
    with style.context({PARAM: other_value}):
        assert mpl.rcParams[PARAM] == other_value
        x = style.context([d])
        with pytest.raises(KeyError):
            with x:
                pass
        assert mpl.rcParams[PARAM] == other_value
