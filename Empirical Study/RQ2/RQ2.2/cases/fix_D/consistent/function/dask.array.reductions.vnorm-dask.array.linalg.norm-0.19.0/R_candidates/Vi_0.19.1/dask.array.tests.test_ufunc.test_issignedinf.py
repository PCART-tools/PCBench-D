def test_issignedinf():
    arr = np.random.randint(-1, 2, size=(20, 20)).astype(float) / 0
    darr = da.from_array(arr, 3)

    assert_eq(np.isneginf(arr), da.isneginf(darr))
    assert_eq(np.isposinf(arr), da.isposinf(darr))
