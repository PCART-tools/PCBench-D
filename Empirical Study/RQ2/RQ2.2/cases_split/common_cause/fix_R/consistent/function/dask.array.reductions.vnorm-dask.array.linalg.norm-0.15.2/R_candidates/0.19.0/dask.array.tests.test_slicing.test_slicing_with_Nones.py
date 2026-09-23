@pytest.mark.parametrize('shape', [(2,), (2, 3), (2, 3, 5)])
@pytest.mark.parametrize('index', [(Ellipsis,),
                                   (None, Ellipsis),
                                   (Ellipsis, None),
                                   (None, Ellipsis, None)])
def test_slicing_with_Nones(shape, index):
    x = np.random.random(shape)
    d = da.from_array(x, chunks=shape)

    assert_eq(x[index], d[index])
