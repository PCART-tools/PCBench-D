@skip_if_no_cuda
@pytest.mark.skipif(torch.cuda.device_count() < 2, reason="Need atleast two GPUs")
def test_verify_nested_modules(setup_rpc):
    model = nn.Sequential(
        nn.Sequential(
            nn.Linear(32, 16).cuda(0),
            nn.Linear(16, 8).cuda(0)
        ),
        nn.Sequential(
            nn.Linear(8, 4).cuda(1),
            nn.Linear(4, 2).cuda(1)
        ),
    )

    pipe = Pipe(model)
    out = pipe(torch.rand(10, 32).cuda(0))
    assert out.local_value().device == torch.device("cuda:1")
    assert out.local_value().size() == torch.Size([10, 2])
