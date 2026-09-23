@pytest.mark.parametrize("checkpoint", ["never", "always", "except_last"])
def test_deferred_batch_norm(checkpoint, setup_rpc):
    bn = nn.BatchNorm2d(3)
    pipe_bn = deepcopy(bn)
    pipe = Pipe(
        nn.Sequential(pipe_bn), chunks=2, checkpoint=checkpoint, deferred_batch_norm=True
    )

    x = torch.rand(4, 3, 10, 10)
    pipe(x).local_value().mean().backward()
    bn(x).mean().backward()

    assert torch.allclose(pipe[0].running_mean, bn.running_mean, atol=1e-4)
    assert torch.allclose(pipe[0].running_var, bn.running_var, atol=1e-4)
