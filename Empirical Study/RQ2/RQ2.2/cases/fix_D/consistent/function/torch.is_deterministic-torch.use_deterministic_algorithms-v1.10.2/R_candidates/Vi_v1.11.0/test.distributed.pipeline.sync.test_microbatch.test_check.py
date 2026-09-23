def test_check():
    check(torch.device("cpu"), torch.tensor(42))
    check(torch.device("cpu"), torch.tensor(4), torch.tensor(2))

    with pytest.raises(TypeError):
        check(torch.device("cpu"), 42)

    with pytest.raises(TypeError):
        check(torch.device("cpu"), "str")

    with pytest.raises(TypeError):
        check(torch.device("cpu"), (torch.tensor(4), 2))
