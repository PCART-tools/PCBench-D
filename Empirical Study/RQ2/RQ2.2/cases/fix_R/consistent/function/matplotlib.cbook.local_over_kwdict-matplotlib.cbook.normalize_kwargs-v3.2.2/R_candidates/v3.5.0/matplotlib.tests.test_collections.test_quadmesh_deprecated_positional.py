@check_figures_equal(extensions=['png'])
def test_quadmesh_deprecated_positional(fig_test, fig_ref):
    # test that positional parameters are still accepted with the old signature
    # and work correctly
    # remove when the old QuadMesh.__init__ signature expires (v3.5+2)
    from matplotlib.collections import QuadMesh

    x = [0, 1, 2, 3.]
    y = [1, 2, 3.]
    X, Y = np.meshgrid(x, y)
    X += 0.2 * Y
    coords = np.stack([X, Y], axis=-1)
    assert coords.shape == (3, 4, 2)
    coords_flat = coords.copy().reshape(-1, 2)
    C = np.linspace(0, 2, 12).reshape(3, 4)

    ax = fig_test.add_subplot()
    ax.set(xlim=(0, 5), ylim=(0, 4))
    qmesh = QuadMesh(coords, antialiased=False, shading='gouraud')
    qmesh.set_array(C)
    ax.add_collection(qmesh)

    ax = fig_ref.add_subplot()
    ax.set(xlim=(0, 5), ylim=(0, 4))
    with pytest.warns(MatplotlibDeprecationWarning):
        qmesh = QuadMesh(4 - 1, 3 - 1, coords.copy().reshape(-1, 2),
                         False, 'gouraud')
    qmesh.set_array(C)
    ax.add_collection(qmesh)
