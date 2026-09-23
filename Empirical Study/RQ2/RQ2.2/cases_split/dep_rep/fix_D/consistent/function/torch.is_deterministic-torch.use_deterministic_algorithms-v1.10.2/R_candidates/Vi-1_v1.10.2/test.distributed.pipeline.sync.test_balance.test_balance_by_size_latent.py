@skip_if_no_cuda
def test_balance_by_size_latent():
    class Expand(nn.Module):
        def __init__(self, times):
            super().__init__()
            self.times = times

        def forward(self, x):
            for i in range(self.times):
                x = x + torch.rand_like(x, requires_grad=True)
            return x

    sample = torch.rand(10, 100, 100)

    model = nn.Sequential(*[Expand(i) for i in [1, 2, 3, 4, 5, 6]])
    balance = balance_by_size(2, model, sample)
    assert balance == [4, 2]

    model = nn.Sequential(*[Expand(i) for i in [6, 5, 4, 3, 2, 1]])
    balance = balance_by_size(2, model, sample)
    assert balance == [2, 4]
