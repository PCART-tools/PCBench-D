@pytest.mark.parametrize("sample_shape", [(), (7,)], ids=str)
@pytest.mark.parametrize("transform_dim", [0, 1, 2])
@pytest.mark.parametrize("base_batch_dim", [0, 1, 2])
@pytest.mark.parametrize("base_event_dim", [0, 1, 2])
@pytest.mark.parametrize("num_transforms", [0, 1, 2, 3])
def test_transformed_distribution(base_batch_dim, base_event_dim, transform_dim,
                                  num_transforms, sample_shape):
    shape = torch.Size([2, 3, 4, 5])
    base_dist = Normal(0, 1)
    base_dist = base_dist.expand(shape[4 - base_batch_dim - base_event_dim:])
    if base_event_dim:
        base_dist = Independent(base_dist, base_event_dim)
    transforms = [AffineTransform(torch.zeros(shape[4 - transform_dim:]), 1),
                  ReshapeTransform((4, 5), (20,)),
                  ReshapeTransform((3, 20), (6, 10))]
    transforms = transforms[:num_transforms]
    transform = ComposeTransform(transforms)

    # Check validation in .__init__().
    if base_batch_dim + base_event_dim < transform.domain.event_dim:
        with pytest.raises(ValueError):
            TransformedDistribution(base_dist, transforms)
        return
    d = TransformedDistribution(base_dist, transforms)

    # Check sampling is sufficiently expanded.
    x = d.sample(sample_shape)
    assert x.shape == sample_shape + d.batch_shape + d.event_shape
    num_unique = len(set(x.reshape(-1).tolist()))
    assert num_unique >= 0.9 * x.numel()

    # Check log_prob shape on full samples.
    log_prob = d.log_prob(x)
    assert log_prob.shape == sample_shape + d.batch_shape

    # Check log_prob shape on partial samples.
    y = x
    while y.dim() > len(d.event_shape):
        y = y[0]
    log_prob = d.log_prob(y)
    assert log_prob.shape == d.batch_shape
