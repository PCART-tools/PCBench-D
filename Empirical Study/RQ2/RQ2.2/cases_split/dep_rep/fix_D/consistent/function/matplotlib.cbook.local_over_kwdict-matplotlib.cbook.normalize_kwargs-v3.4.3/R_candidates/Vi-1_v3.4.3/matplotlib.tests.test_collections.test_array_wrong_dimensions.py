def test_array_wrong_dimensions():
    z = np.arange(12).reshape(3, 4)
    pc = plt.pcolor(z)
    with pytest.raises(ValueError, match="^Collections can only map"):
        pc.set_array(z)
        pc.update_scalarmappable()
    pc = plt.pcolormesh(z)
    pc.set_array(z)  # 2D is OK for Quadmesh
    pc.update_scalarmappable()
