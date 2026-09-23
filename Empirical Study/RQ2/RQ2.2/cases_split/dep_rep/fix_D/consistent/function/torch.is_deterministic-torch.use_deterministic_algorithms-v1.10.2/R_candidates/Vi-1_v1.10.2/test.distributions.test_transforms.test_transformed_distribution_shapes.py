@pytest.mark.parametrize('batch_shape, event_shape, dist', [
    ((4, 4), (), base_dist0),
    ((4,), (4,), base_dist1),
    ((4, 4), (), TransformedDistribution(base_dist0, [transform0])),
    ((4,), (4,), TransformedDistribution(base_dist0, [transform1])),
    ((4,), (4,), TransformedDistribution(base_dist0, [transform0, transform1])),
    ((), (4, 4), TransformedDistribution(base_dist0, [transform0, transform2])),
    ((4,), (4,), TransformedDistribution(base_dist0, [transform1, transform0])),
    ((), (4, 4), TransformedDistribution(base_dist0, [transform1, transform2])),
    ((), (4, 4), TransformedDistribution(base_dist0, [transform2, transform0])),
    ((), (4, 4), TransformedDistribution(base_dist0, [transform2, transform1])),
    ((4,), (4,), TransformedDistribution(base_dist1, [transform0])),
    ((4,), (4,), TransformedDistribution(base_dist1, [transform1])),
    ((), (4, 4), TransformedDistribution(base_dist1, [transform2])),
    ((4,), (4,), TransformedDistribution(base_dist1, [transform0, transform1])),
    ((), (4, 4), TransformedDistribution(base_dist1, [transform0, transform2])),
    ((4,), (4,), TransformedDistribution(base_dist1, [transform1, transform0])),
    ((), (4, 4), TransformedDistribution(base_dist1, [transform1, transform2])),
    ((), (4, 4), TransformedDistribution(base_dist1, [transform2, transform0])),
    ((), (4, 4), TransformedDistribution(base_dist1, [transform2, transform1])),
    ((3, 4, 4), (), base_dist2),
    ((3,), (4, 4), TransformedDistribution(base_dist2, [transform2])),
    ((3,), (4, 4), TransformedDistribution(base_dist2, [transform0, transform2])),
    ((3,), (4, 4), TransformedDistribution(base_dist2, [transform1, transform2])),
    ((3,), (4, 4), TransformedDistribution(base_dist2, [transform2, transform0])),
    ((3,), (4, 4), TransformedDistribution(base_dist2, [transform2, transform1])),
])
def test_transformed_distribution_shapes(batch_shape, event_shape, dist):
    assert dist.batch_shape == batch_shape
    assert dist.event_shape == event_shape
    x = dist.rsample()
    try:
        dist.log_prob(x)  # this should not crash
    except NotImplementedError:
        pytest.skip('Not implemented.')
