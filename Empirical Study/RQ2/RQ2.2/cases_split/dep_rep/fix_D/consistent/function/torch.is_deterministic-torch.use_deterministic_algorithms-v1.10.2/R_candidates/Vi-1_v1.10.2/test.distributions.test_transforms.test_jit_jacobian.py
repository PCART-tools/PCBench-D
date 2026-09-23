@pytest.mark.parametrize('transform', TRANSFORMS_CACHE_INACTIVE, ids=transform_id)
def test_jit_jacobian(transform):
    x = generate_data(transform).requires_grad_()

    def f(x):
        y = transform(x)
        return transform.log_abs_det_jacobian(x, y)

    try:
        traced_f = torch.jit.trace(f, (x,))
    except NotImplementedError:
        pytest.skip('Not implemented.')

    # check on different inputs
    x = generate_data(transform).requires_grad_()
    assert torch.allclose(f(x), traced_f(x), atol=1e-5, equal_nan=True)
