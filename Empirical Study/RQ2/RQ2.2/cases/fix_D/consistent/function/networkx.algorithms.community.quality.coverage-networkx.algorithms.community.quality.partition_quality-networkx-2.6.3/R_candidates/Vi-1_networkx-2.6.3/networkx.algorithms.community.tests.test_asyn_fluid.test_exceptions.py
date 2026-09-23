def test_exceptions():
    test = Graph()
    test.add_node("a")
    pytest.raises(NetworkXError, asyn_fluidc, test, "hi")
    pytest.raises(NetworkXError, asyn_fluidc, test, -1)
    pytest.raises(NetworkXError, asyn_fluidc, test, 3)
    test.add_node("b")
    pytest.raises(NetworkXError, asyn_fluidc, test, 1)
