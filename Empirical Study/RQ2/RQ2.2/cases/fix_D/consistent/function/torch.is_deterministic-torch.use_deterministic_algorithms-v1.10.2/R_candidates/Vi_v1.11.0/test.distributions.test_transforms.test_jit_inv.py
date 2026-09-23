@pytest.mark.parametrize('transform', TRANSFORMS_CACHE_INACTIVE, ids=transform_id)
def test_jit_inv(transform):
    y = generate_data(transform.inv).requires_grad_()

    def f(y):
        return transform.inv(y)

    try:
        traced_f = torch.jit.trace(f, (y,))
    except NotImplementedError:
        pytest.skip('Not implemented.')

    # check on different inputs
    y = generate_data(transform.inv).requires_grad_()
    assert torch.allclose(f(y), traced_f(y), atol=1e-5, equal_nan=True)
