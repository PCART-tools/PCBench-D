@pytest.mark.parametrize("checkpoint", ["never", "always"])
def test_deferred_batch_norm_params(checkpoint, setup_rpc):
    bn = nn.BatchNorm2d(3)
    pipe_bn = deepcopy(bn)
    pipe = Pipe(
        nn.Sequential(pipe_bn), chunks=1, checkpoint=checkpoint, deferred_batch_norm=True
    )

    x = torch.rand(4, 3, 10, 10)
    pipe(x).local_value().mean().backward()
    bn(x).mean().backward()

    assert pipe[0].weight.grad is not None
    assert pipe[0].bias.grad is not None

    assert torch.allclose(pipe[0].weight.grad, bn.weight.grad, atol=1e-4)
    assert torch.allclose(pipe[0].bias.grad, bn.bias.grad, atol=1e-4)
