@pytest.mark.parametrize('transform', ALL_TRANSFORMS, ids=transform_id)
@pytest.mark.parametrize('test_cached', [True, False])
def test_forward_inverse(transform, test_cached):
    x = generate_data(transform).requires_grad_()
    try:
        y = transform(x)
    except NotImplementedError:
        pytest.skip('Not implemented.')
    assert y.shape == transform.forward_shape(x.shape)
    if test_cached:
        x2 = transform.inv(y)  # should be implemented at least by caching
    else:
        try:
            x2 = transform.inv(y.clone())  # bypass cache
        except NotImplementedError:
            pytest.skip('Not implemented.')
    assert x2.shape == transform.inverse_shape(y.shape)
    y2 = transform(x2)
    if transform.bijective:
        # verify function inverse
        assert torch.allclose(x2, x, atol=1e-4, equal_nan=True), '\n'.join([
            '{} t.inv(t(-)) error'.format(transform),
            'x = {}'.format(x),
            'y = t(x) = {}'.format(y),
            'x2 = t.inv(y) = {}'.format(x2),
        ])
    else:
        # verify weaker function pseudo-inverse
        assert torch.allclose(y2, y, atol=1e-4, equal_nan=True), '\n'.join([
            '{} t(t.inv(t(-))) error'.format(transform),
            'x = {}'.format(x),
            'y = t(x) = {}'.format(y),
            'x2 = t.inv(y) = {}'.format(x2),
            'y2 = t(x2) = {}'.format(y2),
        ])
