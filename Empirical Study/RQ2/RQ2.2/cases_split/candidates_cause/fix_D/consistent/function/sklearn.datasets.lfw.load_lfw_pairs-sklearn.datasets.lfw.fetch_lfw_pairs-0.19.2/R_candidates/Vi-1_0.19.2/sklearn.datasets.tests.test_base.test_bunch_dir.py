def test_bunch_dir():
    # check that dir (important for autocomplete) shows attributes
    data = load_iris()
    assert_true("data" in dir(data))
