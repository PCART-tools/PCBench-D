@skip_if_no_cuda
@pytest.mark.skipif(torch.cuda.device_count() < 2, reason="Need atleast two GPUs")
def test_inputs_wrong_device(setup_rpc):
    class Module1(nn.Module):
        def __init__(self):
            super().__init__()
            self.param = torch.nn.Parameter(torch.rand(5))

        def forward(self, a, b):
            return a + b + self.param, b

    # Start inputs on wrong device and ensure Pipe moves them correctly.
    a = torch.rand(10).cuda(1)
    b = torch.rand(10).cuda(1)
    model = Pipe(nn.Sequential(Module1().cuda(0), Module1().cuda(1)), chunks=2)
    with pytest.raises(ValueError, match='All inputs should be on the same device as the first partition'):
        model(a, b)
