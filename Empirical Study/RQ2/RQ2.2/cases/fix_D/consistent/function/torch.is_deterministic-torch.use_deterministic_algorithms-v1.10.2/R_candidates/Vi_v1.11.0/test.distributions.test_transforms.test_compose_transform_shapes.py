def test_compose_transform_shapes():
    transform0 = ExpTransform()
    transform1 = SoftmaxTransform()
    transform2 = LowerCholeskyTransform()

    assert transform0.event_dim == 0
    assert transform1.event_dim == 1
    assert transform2.event_dim == 2
    assert ComposeTransform([transform0, transform1]).event_dim == 1
    assert ComposeTransform([transform0, transform2]).event_dim == 2
    assert ComposeTransform([transform1, transform2]).event_dim == 2
