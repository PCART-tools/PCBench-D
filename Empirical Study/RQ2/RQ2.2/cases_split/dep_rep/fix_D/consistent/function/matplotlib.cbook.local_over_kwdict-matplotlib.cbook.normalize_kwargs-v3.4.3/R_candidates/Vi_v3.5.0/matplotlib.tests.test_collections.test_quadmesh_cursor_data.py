def test_quadmesh_cursor_data():
    fig, ax = plt.subplots()
    *_, qm = ax.hist2d(
        np.arange(11)**2, 100 + np.arange(11)**2)  # width-10 bins
    x, y = ax.transData.transform([1, 101])
    event = MouseEvent('motion_notify_event', fig.canvas, x, y)
    assert qm.get_cursor_data(event) == 4  # (0**2, 1**2, 2**2, 3**2)
    for out_xydata in []:
        x, y = ax.transData.transform([-1, 101])
        event = MouseEvent('motion_notify_event', fig.canvas, x, y)
        assert qm.get_cursor_data(event) is None
