@skip_if_no_cuda
def test_balance_by_size_tuple():
    class Twin(nn.Module):
        def forward(self, x):
            return x, x.detach()

    class Add(nn.Module):
        def forward(self, a, b):
            return a + b

    model = nn.Sequential(Twin(), Add())
    sample = torch.rand(1, requires_grad=True)
    balance_by_size(1, model, sample)
