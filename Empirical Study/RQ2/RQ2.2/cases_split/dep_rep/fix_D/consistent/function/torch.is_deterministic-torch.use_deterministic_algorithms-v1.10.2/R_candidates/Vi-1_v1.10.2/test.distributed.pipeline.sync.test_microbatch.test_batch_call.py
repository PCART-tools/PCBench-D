def test_batch_call():
    a = Batch(torch.tensor(42))
    b = Batch((torch.tensor(42), torch.tensor(21)))

    def f(x):
        return x

    def g(x, y):
        return x, y

    assert a.call(f).atomic
    assert not b.call(g).atomic
