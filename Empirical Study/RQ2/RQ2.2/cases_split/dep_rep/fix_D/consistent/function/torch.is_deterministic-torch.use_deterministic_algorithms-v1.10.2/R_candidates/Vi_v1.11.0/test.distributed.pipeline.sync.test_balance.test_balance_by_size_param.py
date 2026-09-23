@skip_if_no_cuda
def test_balance_by_size_param():
    model = nn.Sequential(*[nn.Linear(i + 1, i + 2) for i in range(6)])
    sample = torch.rand(7, 1)
    balance = balance_by_size(2, model, sample, param_scale=100)
    assert balance == [4, 2]

    model = nn.Sequential(*[nn.Linear(i + 2, i + 1) for i in reversed(range(6))])
    sample = torch.rand(1, 7)
    balance = balance_by_size(2, model, sample, param_scale=100)
    assert balance == [2, 4]
