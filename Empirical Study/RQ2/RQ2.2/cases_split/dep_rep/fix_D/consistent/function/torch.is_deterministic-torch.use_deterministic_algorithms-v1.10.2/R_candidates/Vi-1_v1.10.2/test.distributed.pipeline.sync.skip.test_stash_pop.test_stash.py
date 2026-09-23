def test_stash(skip_tracker):
    @skippable(stash=["foo"])
    class Stash(nn.Module):
        def forward(self, input):
            yield stash("foo", input)
            return input * 2  # noqa: B901

    l1 = Stash()

    assert len(skip_tracker.tensors) == 0

    with use_skip_tracker(skip_tracker):
        l1(torch.tensor(42))

    assert len(skip_tracker.tensors) == 1
