@pytest.mark.parametrize("train", [True, False], ids=["train", "eval"])
def test_no_portal_without_pipe(train, monkeypatch, setup_rpc):
    def deny(*args, **kwargs):
        raise AssertionError("tried to create Portal without Pipe")

    monkeypatch.setattr("torch.distributed.pipeline.sync.skip.portal.Portal.__init__", deny)

    model = nn.Sequential(Stash(), Pop())

    input = torch.rand(10, requires_grad=True)

    if train:
        model.train()
        output = model(input)
        output.norm().backward()
    else:
        model.eval()
        with torch.no_grad():
            model(input)
