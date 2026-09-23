@pytest.mark.parametrize("momentum", [0.1, None])
def test_running_stats(momentum):
    bn = nn.BatchNorm2d(3, momentum=momentum)
    dbn = DeferredBatchNorm.convert_deferred_batch_norm(deepcopy(bn), chunks=CHUNKS)

    input = torch.rand(16, 3, 224, 224)
    input = tilt_dist(input)

    bn(input)
    chunked_forward(dbn, input)

    assert torch.allclose(bn.running_mean, dbn.running_mean, atol=1e-4)
    assert torch.allclose(bn.running_var, dbn.running_var, atol=1e-4)
