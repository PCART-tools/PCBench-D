def test_picking():
    fig, ax = plt.subplots()
    col = ax.scatter([0], [0], [1000], picker=True)
    fig.savefig(io.BytesIO(), dpi=fig.dpi)
    mouse_event = SimpleNamespace(x=325, y=240)
    found, indices = col.contains(mouse_event)
    assert found
    assert_array_equal(indices['ind'], [0])
