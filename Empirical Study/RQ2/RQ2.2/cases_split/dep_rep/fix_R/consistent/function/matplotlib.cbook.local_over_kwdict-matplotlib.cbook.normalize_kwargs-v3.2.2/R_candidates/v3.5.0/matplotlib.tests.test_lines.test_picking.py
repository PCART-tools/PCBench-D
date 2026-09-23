def test_picking():
    fig, ax = plt.subplots()
    mouse_event = SimpleNamespace(x=fig.bbox.width // 2,
                                  y=fig.bbox.height // 2 + 15)

    # Default pickradius is 5, so event should not pick this line.
    l0, = ax.plot([0, 1], [0, 1], picker=True)
    found, indices = l0.contains(mouse_event)
    assert not found

    # But with a larger pickradius, this should be picked.
    l1, = ax.plot([0, 1], [0, 1], picker=True, pickradius=20)
    found, indices = l1.contains(mouse_event)
    assert found
    assert_array_equal(indices['ind'], [0])

    # And if we modify the pickradius after creation, it should work as well.
    l2, = ax.plot([0, 1], [0, 1], picker=True)
    found, indices = l2.contains(mouse_event)
    assert not found
    l2.set_pickradius(20)
    found, indices = l2.contains(mouse_event)
    assert found
    assert_array_equal(indices['ind'], [0])
