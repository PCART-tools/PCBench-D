def test_quadmesh_set_array_validation():
    x = np.arange(11)
    y = np.arange(8)
    z = np.random.random((7, 10))
    fig, ax = plt.subplots()
    coll = ax.pcolormesh(x, y, z)

    # Test deprecated warning when faulty shape is passed.
    with pytest.warns(MatplotlibDeprecationWarning):
        coll.set_array(z.reshape(10, 7))

    z = np.arange(54).reshape((6, 9))
    with pytest.raises(TypeError, match=r"Dimensions of A \(6, 9\) "
                       r"are incompatible with X \(11\) and/or Y \(8\)"):
        coll.set_array(z)
    with pytest.raises(TypeError, match=r"Dimensions of A \(54,\) "
                       r"are incompatible with X \(11\) and/or Y \(8\)"):
        coll.set_array(z.ravel())

    x = np.arange(10)
    y = np.arange(7)
    z = np.random.random((7, 10))
    fig, ax = plt.subplots()
    coll = ax.pcolormesh(x, y, z, shading='gouraud')
