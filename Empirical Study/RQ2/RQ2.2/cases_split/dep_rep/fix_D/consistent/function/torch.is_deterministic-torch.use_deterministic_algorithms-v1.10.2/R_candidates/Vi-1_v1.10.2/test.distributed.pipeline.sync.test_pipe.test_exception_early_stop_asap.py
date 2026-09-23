def test_exception_early_stop_asap(setup_rpc):
    """Even the first partitions have finished to process, the partition before
    the failed partition should be killed as soon as possible.
    """

    class ExpectedException(Exception):
        pass

    class Pass(nn.Module):
        def forward(self, x):
            return x

    counter = 0

    class Counter(nn.Module):
        def forward(self, x):
            time.sleep(0.1)

            nonlocal counter
            counter += 1

            return x

    class Raise(nn.Module):
        def forward(self, x):
            raise ExpectedException()

    model = nn.Sequential(Pass(), Pass(), Counter(), Raise())
    model = Pipe(model, chunks=3)

    with pytest.raises(ExpectedException):
        model(torch.rand(3))

    # If the early stop doesn't work, it would be 3 instead.
    assert counter == 2
