def test_not_training():
    class AssertTraining(nn.Module):
        def forward(self, x):
            assert self.training
            return x

    model = nn.Sequential(AssertTraining())

    model.eval()
    assert not model.training

    sample = torch.rand(1)
    balance_by_time(1, model, sample, device="cpu")

    assert not model.training
