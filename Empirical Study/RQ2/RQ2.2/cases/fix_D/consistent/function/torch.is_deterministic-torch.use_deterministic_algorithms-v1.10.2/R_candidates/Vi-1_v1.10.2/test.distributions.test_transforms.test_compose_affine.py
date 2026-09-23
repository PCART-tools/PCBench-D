@pytest.mark.parametrize("event_dims",
                         [(0,), (1,), (2, 3), (0, 1, 2), (1, 2, 0), (2, 0, 1)],
                         ids=str)
def test_compose_affine(event_dims):
    transforms = [AffineTransform(torch.zeros((1,) * e), 1, event_dim=e) for e in event_dims]
    transform = ComposeTransform(transforms)
    assert transform.codomain.event_dim == max(event_dims)
    assert transform.domain.event_dim == max(event_dims)

    base_dist = Normal(0, 1)
    if transform.domain.event_dim:
        base_dist = base_dist.expand((1,) * transform.domain.event_dim)
    dist = TransformedDistribution(base_dist, transform.parts)
    assert dist.support.event_dim == max(event_dims)

    base_dist = Dirichlet(torch.ones(5))
    if transform.domain.event_dim > 1:
        base_dist = base_dist.expand((1,) * (transform.domain.event_dim - 1))
    dist = TransformedDistribution(base_dist, transforms)
    assert dist.support.event_dim == max(1, max(event_dims))
