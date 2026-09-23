def test_attributes():
    a = delayed(2 + 1j)
    assert a.real.compute() == 2
    assert a.imag.compute() == 1
    assert (a.real + a.imag).compute() == 3
