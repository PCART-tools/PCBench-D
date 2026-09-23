@pytest.mark.skipif(not torch.cuda.is_available(), reason="cuda required")
def test_merged_partitions(setup_rpc):
    a = nn.Linear(1, 1).to(0)
    b = nn.Sequential(nn.Linear(1, 1), nn.Linear(1, 2)).to(0)
    c = nn.Linear(1, 1)
    d = nn.Linear(1, 2)

    model = nn.Sequential(a, b, c, d)
    model = Pipe(model)

    assert isinstance(model.partitions, nn.ModuleList)
    assert isinstance(model.partitions[0], PipeSequential)
    assert isinstance(model.partitions[1], PipeSequential)
    assert list(model.partitions[0]) == [a, b[0], b[1]]
    assert list(model.partitions[1]) == [c]
    assert list(model.partitions[2]) == [d]
