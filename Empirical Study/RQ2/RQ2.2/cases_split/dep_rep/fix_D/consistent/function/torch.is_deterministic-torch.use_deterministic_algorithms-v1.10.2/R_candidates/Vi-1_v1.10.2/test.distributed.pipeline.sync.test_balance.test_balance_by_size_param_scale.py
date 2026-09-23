@skip_if_no_cuda
def test_balance_by_size_param_scale():
    class Tradeoff(nn.Module):
        def __init__(self, param_size, latent_size):
            super().__init__()
            self.fc = nn.Linear(param_size, param_size)
            self.latent_size = latent_size

        def forward(self, x):
            for i in range(self.latent_size):
                x = x + torch.rand_like(x, requires_grad=True)
            return x

    model = nn.Sequential(
        Tradeoff(param_size=1, latent_size=6),
        Tradeoff(param_size=2, latent_size=5),
        Tradeoff(param_size=3, latent_size=4),
        Tradeoff(param_size=4, latent_size=3),
        Tradeoff(param_size=5, latent_size=2),
        Tradeoff(param_size=6, latent_size=1),
    )

    sample = torch.rand(1, requires_grad=True)

    balance = balance_by_size(2, model, sample, param_scale=0)
    assert balance == [2, 4]

    balance = balance_by_size(2, model, sample, param_scale=100)
    assert balance == [4, 2]
