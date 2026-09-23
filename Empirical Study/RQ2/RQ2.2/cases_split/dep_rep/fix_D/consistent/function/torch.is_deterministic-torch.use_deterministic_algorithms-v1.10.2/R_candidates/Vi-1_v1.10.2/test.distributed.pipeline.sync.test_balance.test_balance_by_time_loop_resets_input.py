def test_balance_by_time_loop_resets_input():
    # nn.Flatten was introduced at PyTorch 1.2.0.
    class Flatten(nn.Module):
        def forward(self, x):
            return x.flatten(1)

    model = nn.Sequential(nn.Conv2d(3, 2, 1), Flatten(), nn.Linear(128, 10))
    sample = torch.rand(10, 3, 8, 8)
    balance = balance_by_time(2, model, sample, device="cpu")
    assert balance == [1, 2]
