def test_pop():
    @skippable(stash=["foo"])
    class Stash(nn.Module):
        def forward(self, input):
            yield stash("foo", input)
            return input * 2  # noqa: B901

    @skippable(pop=["foo"])
    class Pop(nn.Module):
        def forward(self, input):
            foo = yield pop("foo")
            return foo

    l1 = Stash()
    l2 = Pop()

    output = l2(l1(torch.tensor(42)))

    assert output.item() == 42
