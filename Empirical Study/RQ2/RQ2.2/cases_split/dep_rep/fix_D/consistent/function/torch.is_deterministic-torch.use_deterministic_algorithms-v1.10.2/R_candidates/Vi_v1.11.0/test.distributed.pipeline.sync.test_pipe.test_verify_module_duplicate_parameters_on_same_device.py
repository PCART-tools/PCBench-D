def test_verify_module_duplicate_parameters_on_same_device(setup_rpc):
    class Surrogate(nn.Module):
        def __init__(self, module):
            super().__init__()
            self.module = module

    conv = nn.Conv2d(3, 3, 1)
    model = nn.Sequential(Surrogate(conv), Surrogate(conv))

    Pipe(model)
