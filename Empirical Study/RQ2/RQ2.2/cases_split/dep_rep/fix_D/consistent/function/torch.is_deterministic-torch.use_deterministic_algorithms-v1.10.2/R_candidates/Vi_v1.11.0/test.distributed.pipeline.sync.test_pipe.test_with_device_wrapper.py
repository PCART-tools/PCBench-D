@skip_if_no_cuda
@pytest.mark.skipif(torch.cuda.device_count() < 2, reason="Need atleast two GPUs")
def test_with_device_wrapper(setup_rpc):
    fc1 = nn.Linear(16, 8).cuda(0)
    fc2 = nn.Linear(8, 4).cuda(1)
    dropout = nn.Dropout()

    model = nn.Sequential(fc1, fc2, WithDevice(dropout, 'cuda:1'))
    model = Pipe(model, chunks=8)
    assert torch.device('cuda:1') == model(torch.rand(16, 16).cuda(0)).local_value().device
    assert [torch.device('cuda:0'), torch.device('cuda:1')] == model.devices

    model = nn.Sequential(fc1, WithDevice(dropout, 'cuda:1'))
    model = Pipe(model, chunks=8)
    assert torch.device('cuda:1') == model(torch.rand(16, 16).cuda(0)).local_value().device
    assert [torch.device('cuda:0'), torch.device('cuda:1')] == model.devices

    model = nn.Sequential(fc1, WithDevice(fc2, 'cuda:0'))
    model = Pipe(model, chunks=8)
    assert torch.device('cuda:0') == model(torch.rand(16, 16).cuda(0)).local_value().device
    assert [torch.device('cuda:0')] == model.devices
    assert torch.device('cuda:0') == fc2.weight.device
