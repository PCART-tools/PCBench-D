def test_pop_not_stashed():
    @skippable(pop=["foo"])
    class Pop(nn.Module):
        def forward(self, input):
            yield pop("foo")

    l1 = Pop()

    with pytest.raises(RuntimeError):
        l1(torch.tensor(42))
