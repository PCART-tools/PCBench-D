def test_colorbar_get_ticks():
    # test feature for #5792
    plt.figure()
    data = np.arange(1200).reshape(30, 40)
    levels = [0, 200, 400, 600, 800, 1000, 1200]

    plt.contourf(data, levels=levels)

    # testing getter for user set ticks
    userTicks = plt.colorbar(ticks=[0, 600, 1200])
    assert userTicks.get_ticks().tolist() == [0, 600, 1200]

    # testing for getter after calling set_ticks
    userTicks.set_ticks([600, 700, 800])
    assert userTicks.get_ticks().tolist() == [600, 700, 800]

    # testing for getter after calling set_ticks with some ticks out of bounds
    userTicks.set_ticks([600, 1300, 1400, 1500])
    assert userTicks.get_ticks().tolist() == [600]

    # testing getter when no ticks are assigned
    defTicks = plt.colorbar(orientation='horizontal')
    assert defTicks.get_ticks().tolist() == levels
