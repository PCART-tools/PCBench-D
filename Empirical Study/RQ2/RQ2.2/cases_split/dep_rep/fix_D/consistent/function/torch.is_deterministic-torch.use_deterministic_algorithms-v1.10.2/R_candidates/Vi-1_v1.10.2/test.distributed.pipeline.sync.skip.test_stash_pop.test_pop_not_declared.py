def test_pop_not_declared():
    @skippable(stash=["foo"])
    class Stash(nn.Module):
        def forward(self, input):
            yield stash("foo", input)
            return input * 2  # noqa: B901

    @skippable()
    class Pop(nn.Module):
        def forward(self, input):
            foo = yield pop("foo")
            return foo

    l1 = Stash()
    l2 = Pop()

    latent = l1(torch.tensor(42))

    with pytest.raises(RuntimeError):
        l2(latent)
