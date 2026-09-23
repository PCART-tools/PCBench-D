@pytest.mark.parametrize("batch_shape", [(), (6,), (5, 4)], ids=str)
def test_compose_reshape(batch_shape):
    transforms = [ReshapeTransform((), ()),
                  ReshapeTransform((2,), (1, 2)),
                  ReshapeTransform((3, 1, 2), (6,)),
                  ReshapeTransform((6,), (2, 3))]
    transform = ComposeTransform(transforms)
    assert transform.codomain.event_dim == 2
    assert transform.domain.event_dim == 2
    data = torch.randn(batch_shape + (3, 2))
    assert transform(data).shape == batch_shape + (2, 3)

    dist = TransformedDistribution(Normal(data, 1), transforms)
    assert dist.batch_shape == batch_shape
    assert dist.event_shape == (2, 3)
    assert dist.support.event_dim == 2
