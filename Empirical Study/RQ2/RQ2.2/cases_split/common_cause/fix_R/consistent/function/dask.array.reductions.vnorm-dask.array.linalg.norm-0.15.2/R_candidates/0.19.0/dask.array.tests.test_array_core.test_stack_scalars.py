def test_stack_scalars():
    d = da.arange(4, chunks=2)

    s = da.stack([d.mean(), d.sum()])

    assert s.compute().tolist() == [np.arange(4).mean(), np.arange(4).sum()]
