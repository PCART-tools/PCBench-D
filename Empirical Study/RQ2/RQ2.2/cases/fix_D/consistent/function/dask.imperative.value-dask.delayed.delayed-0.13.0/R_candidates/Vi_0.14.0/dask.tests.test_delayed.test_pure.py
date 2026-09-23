def test_pure():
    v1 = delayed(add, pure=True)(1, 2)
    v2 = delayed(add, pure=True)(1, 2)
    assert v1.key == v2.key

    myrand = delayed(random)
    assert myrand().key != myrand().key
