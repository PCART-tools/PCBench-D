@pytest.mark.parametrize('func', [da.cumsum, da.cumprod,
                                  da.argmin, da.argmax,
                                  da.min, da.max,
                                  da.nansum, da.nanmax])
def test_regres_3940(func):
    a = da.ones((5,2), chunks=(2,2))
    assert func(a).name != func(a + 1).name
    assert func(a, axis=0).name != func(a).name
    assert func(a, axis=0).name != func(a, axis=1).name
