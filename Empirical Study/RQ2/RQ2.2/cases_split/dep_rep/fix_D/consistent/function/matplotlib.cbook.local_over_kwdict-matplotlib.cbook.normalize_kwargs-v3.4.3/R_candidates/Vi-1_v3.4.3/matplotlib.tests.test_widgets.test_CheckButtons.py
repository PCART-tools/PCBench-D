def test_CheckButtons():
    ax = get_ax()
    check = widgets.CheckButtons(ax, ('a', 'b', 'c'), (True, False, True))
    assert check.get_status() == [True, False, True]
    check.set_active(0)
    assert check.get_status() == [False, False, True]

    cid = check.on_clicked(lambda: None)
    check.disconnect(cid)
