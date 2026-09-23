@pytest.mark.xfail
def test_iterators():
    a = delayed(1)
    b = delayed(2)
    c = delayed(sum)(iter([a, b]))

    assert c.compute() == 3

    def f(seq):
        assert isinstance(seq, Iterator)
        return sum(seq)

    c = delayed(f)(iter([a, b]))
    assert c.compute() == 3
