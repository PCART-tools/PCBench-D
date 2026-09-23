def test_stash_none():
    @skippable(stash=["foo"])
    class Stash(nn.Module):
        def forward(self, input):
            yield stash("foo", None)
            return input * 2  # noqa: B901

    l1 = Stash()
    l1(torch.tensor(42))
