def test_stash_not_declared():
    @skippable()
    class Stash(nn.Module):
        def forward(self, input):
            yield stash("foo", input)
            return input * 2  # noqa: B901

    l1 = Stash()

    with pytest.raises(RuntimeError):
        l1(torch.tensor(42))
