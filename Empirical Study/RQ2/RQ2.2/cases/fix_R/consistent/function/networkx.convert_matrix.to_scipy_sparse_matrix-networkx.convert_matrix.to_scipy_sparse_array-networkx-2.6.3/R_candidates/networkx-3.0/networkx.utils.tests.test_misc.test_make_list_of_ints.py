def test_make_list_of_ints():
    mylist = [1, 2, 3.0, 42, -2]
    assert make_list_of_ints(mylist) is mylist
    assert make_list_of_ints(mylist) == mylist
    assert type(make_list_of_ints(mylist)[2]) is int
    pytest.raises(nx.NetworkXError, make_list_of_ints, [1, 2, 3, "kermit"])
    pytest.raises(nx.NetworkXError, make_list_of_ints, [1, 2, 3.1])
