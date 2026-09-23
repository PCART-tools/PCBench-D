    @pytest.mark.parametrize('kwargs, errortype, match', [
        ({'foo': 0}, TypeError,
         re.escape("set_params() got an unexpected keyword argument 'foo'")),
        ({'steps': [2, 1]}, ValueError, "steps argument must be an increasing"),
        ({'steps': 2}, ValueError, "steps argument must be an increasing"),
        ({'steps': [2, 11]}, ValueError, "steps argument must be an increasing"),
    ])
    def test_errors(self, kwargs, errortype, match):
        with pytest.raises(errortype, match=match):
            mticker.MaxNLocator(**kwargs)
