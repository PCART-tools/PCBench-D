def test_loads_dumps_bunch():
    bunch = Bunch(x="x")
    bunch_from_pkl = loads(dumps(bunch))
    bunch_from_pkl.x = "y"
    assert_equal(bunch_from_pkl['x'], bunch_from_pkl.x)
