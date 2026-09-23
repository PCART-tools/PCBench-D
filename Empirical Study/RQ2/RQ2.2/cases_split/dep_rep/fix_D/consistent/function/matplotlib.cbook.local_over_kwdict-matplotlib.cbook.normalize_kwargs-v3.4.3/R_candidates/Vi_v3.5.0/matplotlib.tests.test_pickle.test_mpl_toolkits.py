def test_mpl_toolkits():
    ax = parasite_axes.host_axes([0, 0, 1, 1])
    assert type(pickle.loads(pickle.dumps(ax))) == parasite_axes.HostAxes
