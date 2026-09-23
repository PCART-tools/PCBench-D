@skip_if_no_cuda
def test_verify_module_params_on_same_device(setup_rpc):
    class Surrogate(nn.Module):
        def __init__(self, param1, param2):
            super().__init__()
            self.param1 = param1
            self.param2 = param2

    conv1 = nn.Conv2d(3, 3, 1)
    conv2 = nn.Conv2d(3, 3, 1)
    model = nn.Sequential(Surrogate(conv1, conv2.cuda()))

    with pytest.raises(
        ValueError,
        match=r'should have all parameters on a single device, please use .to\(\)'
            ' to place the module on a single device'):
        Pipe(model)
