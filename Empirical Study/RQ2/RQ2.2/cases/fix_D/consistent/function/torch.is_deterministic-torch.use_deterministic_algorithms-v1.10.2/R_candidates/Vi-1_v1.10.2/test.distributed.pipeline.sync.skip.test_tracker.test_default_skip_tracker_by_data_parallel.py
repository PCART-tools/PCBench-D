@pytest.mark.skipif(not torch.cuda.is_available(), reason="cuda required")
def test_default_skip_tracker_by_data_parallel():
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

    model = nn.Sequential(Stash(), Pop())
    model = nn.DataParallel(model, device_ids=[0, 0], output_device=0)

    input = torch.rand(10, device=0)
    output = model(input)

    assert torch.allclose(output, input)
