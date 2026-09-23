def test_declare_but_not_use():
    @skippable(stash=["foo"])
    class Stash(nn.Module):
        def forward(self, input):
            return input * 2

    @skippable(pop=["foo"])
    class Pop(nn.Module):
        def forward(self, input):
            return input * 3

    l1 = Stash()
    l2 = Pop()

    with pytest.raises(RuntimeError):
        l1(torch.tensor(42))

    with pytest.raises(RuntimeError):
        l2(torch.tensor(42))
