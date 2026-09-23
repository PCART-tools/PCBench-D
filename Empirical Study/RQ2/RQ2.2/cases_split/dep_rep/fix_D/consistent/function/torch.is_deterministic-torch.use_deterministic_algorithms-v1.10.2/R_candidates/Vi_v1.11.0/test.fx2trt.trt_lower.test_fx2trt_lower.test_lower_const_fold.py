def test_lower_const_fold():
    class TestModule(torch.nn.Module):
        def __init__(self):
            self.a = torch.randn(1)

        def forward(self, x):
            return (torch.sqrt(x), self.a)

    lower = Lowerer.create(LowerSetting())
    assert lower(TestModule(), [2, 2])
