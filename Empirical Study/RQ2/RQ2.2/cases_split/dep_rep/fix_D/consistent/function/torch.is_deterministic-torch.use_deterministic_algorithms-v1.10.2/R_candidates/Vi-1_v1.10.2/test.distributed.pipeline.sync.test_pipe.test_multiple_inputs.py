@pytest.mark.parametrize("checkpoint", ["never", "always", "except_last"])
@skip_if_no_cuda
def test_multiple_inputs(checkpoint, setup_rpc):
    class Module1(nn.Module):
        def forward(self, a, b, c):
            return a + b + c, a * b * c

    class Module2(nn.Module):
        def forward(self, a, b):
            return a + b

    model = Pipe(nn.Sequential(Module1().cuda(0), Module2().cuda(0)), chunks=2, checkpoint=checkpoint)
    t = torch.rand(10)
    res = model(t, t, t).local_value()
    assert torch.equal(res, (t + t + t) + (t * t * t))
