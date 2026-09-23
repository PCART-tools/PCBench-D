def _allclose(a, b):
    if isinstance(a, tuple):
        assert isinstance(b, tuple)
        result = True
        for a_inner, b_inner in zip(a, b):
            result = result and torch.allclose(a_inner, b_inner)
        return result
    elif isinstance(a, torch.Tensor):
        assert isinstance(b, torch.Tensor)
        return torch.allclose(a, b)
    raise AssertionError('unhandled type')
