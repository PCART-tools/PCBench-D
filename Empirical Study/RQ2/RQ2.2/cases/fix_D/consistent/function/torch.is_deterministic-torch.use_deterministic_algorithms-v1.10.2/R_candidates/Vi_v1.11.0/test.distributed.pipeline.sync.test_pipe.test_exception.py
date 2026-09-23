def test_exception(setup_rpc):
    class ExpectedException(Exception):
        pass

    class Raise(nn.Module):
        def forward(self, *_):
            raise ExpectedException()

    model = nn.Sequential(Raise())
    model = Pipe(model, chunks=1)

    with pytest.raises(ExpectedException):
        model(torch.rand(1))
