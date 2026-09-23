def test_exception_no_hang(setup_rpc):
    # In v0.0.2, once a failed partition receives a normal message
    # (non-closing) for the next micro-batch, a hang occured. The reason was
    # that a failed partition didn't call in_queue.task_done() on a normal
    # message. So the former partition was blocked at out_queue.join() for the
    # next of next micro-batch.
    class ExpectedException(Exception):
        pass

    class Pass(nn.Module):
        def forward(self, x):
            return x

    class Raise(nn.Module):
        def forward(self, x):
            raise ExpectedException()

    model = nn.Sequential(Pass(), Pass(), Raise())
    model = Pipe(model, chunks=3)

    with pytest.raises(ExpectedException):
        model(torch.rand(3))
