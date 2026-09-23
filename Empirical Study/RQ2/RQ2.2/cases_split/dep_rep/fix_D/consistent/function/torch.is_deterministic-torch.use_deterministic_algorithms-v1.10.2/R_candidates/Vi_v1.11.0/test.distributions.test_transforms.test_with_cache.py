@pytest.mark.parametrize('transform', ALL_TRANSFORMS, ids=transform_id)
def test_with_cache(transform):
    if transform._cache_size == 0:
        transform = transform.with_cache(1)
    assert transform._cache_size == 1
    x = generate_data(transform).requires_grad_()
    try:
        y = transform(x)
    except NotImplementedError:
        pytest.skip('Not implemented.')
    y2 = transform(x)
    assert y2 is y
