@pytest.mark.parametrize('flat_ref, kwargs', [
    (True, {}),
    (False, {}),
    (True, dict(antialiased=False)),
    (False, dict(transform='__initialization_delayed__')),
])
@check_figures_equal(extensions=['png'])
def test_quadmesh_deprecated_signature(
        fig_test, fig_ref, flat_ref, kwargs):
    # test that the new and old quadmesh signature produce the same results
    # remove when the old QuadMesh.__init__ signature expires (v3.5+2)
    from matplotlib.collections import QuadMesh

    x = [0, 1, 2, 3.]
    y = [1, 2, 3.]
    X, Y = np.meshgrid(x, y)
    X += 0.2 * Y
    coords = np.stack([X, Y], axis=-1)
    assert coords.shape == (3, 4, 2)
    C = np.linspace(0, 2, 6).reshape(2, 3)

    ax = fig_test.add_subplot()
    ax.set(xlim=(0, 5), ylim=(0, 4))
    if 'transform' in kwargs:
        kwargs['transform'] = mtransforms.Affine2D().scale(1.2) + ax.transData
    qmesh = QuadMesh(coords, **kwargs)
    qmesh.set_array(C)
    ax.add_collection(qmesh)
    assert qmesh._shading == 'flat'

    ax = fig_ref.add_subplot()
    ax.set(xlim=(0, 5), ylim=(0, 4))
    if 'transform' in kwargs:
        kwargs['transform'] = mtransforms.Affine2D().scale(1.2) + ax.transData
    with pytest.warns(MatplotlibDeprecationWarning):
        qmesh = QuadMesh(4 - 1, 3 - 1,
                         coords.copy().reshape(-1, 2) if flat_ref else coords,
                         **kwargs)
    qmesh.set_array(C.flatten() if flat_ref else C)
    ax.add_collection(qmesh)
    assert qmesh._shading == 'flat'
