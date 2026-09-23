@pytest.mark.parametrize(
    "image_cls,x,y,a", [
        (NonUniformImage,
         np.arange(3.), np.arange(4.), np.arange(12.).reshape((4, 3))),
        (PcolorImage,
         np.arange(3.), np.arange(4.), np.arange(6.).reshape((3, 2))),
    ])
def test_setdata_xya(image_cls, x, y, a):
    ax = plt.gca()
    im = image_cls(ax)
    im.set_data(x, y, a)
    x[0] = y[0] = a[0, 0] = 9.9
    assert im._A[0, 0] == im._Ax[0] == im._Ay[0] == 0, 'value changed'
    im.set_data(x, y, a.reshape((*a.shape, -1)))  # Just a smoketest.
