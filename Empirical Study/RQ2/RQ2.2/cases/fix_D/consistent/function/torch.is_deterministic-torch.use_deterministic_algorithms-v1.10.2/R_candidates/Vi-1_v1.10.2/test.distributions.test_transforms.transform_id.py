def transform_id(x):
    assert isinstance(x, Transform)
    name = f'Inv({type(x._inv).__name__})' if isinstance(x, _InverseTransform) else f'{type(x).__name__}'
    return f'{name}(cache_size={x._cache_size})'
