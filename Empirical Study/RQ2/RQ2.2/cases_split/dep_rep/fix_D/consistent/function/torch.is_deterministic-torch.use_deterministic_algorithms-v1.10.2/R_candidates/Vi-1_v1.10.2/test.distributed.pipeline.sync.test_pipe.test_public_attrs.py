def test_public_attrs(setup_rpc):
    class MyString:
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return self.value

    model = nn.Sequential(nn.Linear(1, 1))
    pipe = Pipe(model, chunks=42.000, checkpoint=MyString("always"))

    assert pipe.devices == [torch.device("cpu")]
    assert pipe.chunks == 42
    assert isinstance(pipe.chunks, int)
    assert pipe.checkpoint == "always"
    assert isinstance(pipe.checkpoint, str)
