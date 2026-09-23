def test_callbacks():
    def func(artist):
        func.counter += 1

    func.counter = 0

    art = martist.Artist()
    oid = art.add_callback(func)
    assert func.counter == 0
    art.pchanged()  # must call the callback
    assert func.counter == 1
    art.set_zorder(10)  # setting a property must also call the callback
    assert func.counter == 2
    art.remove_callback(oid)
    art.pchanged()  # must not call the callback anymore
    assert func.counter == 2
