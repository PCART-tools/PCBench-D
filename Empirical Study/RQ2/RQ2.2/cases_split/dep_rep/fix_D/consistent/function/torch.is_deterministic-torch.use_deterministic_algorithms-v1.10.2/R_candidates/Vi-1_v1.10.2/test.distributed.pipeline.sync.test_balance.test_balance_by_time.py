@pytest.mark.parametrize("device", devices)
@pytest.mark.skip(reason="Flaky due to time.sleep()")
def test_balance_by_time(device):
    class Delay(nn.Module):
        def __init__(self, seconds):
            super().__init__()
            self.seconds = seconds

        def forward(self, x):
            time.sleep(self.seconds)
            return x

    model = nn.Sequential(*[Delay(i / 10) for i in [1, 2, 3, 4, 5, 6]])
    sample = torch.rand(1)
    balance = balance_by_time(2, model, sample, device=device)
    assert balance == [4, 2]
