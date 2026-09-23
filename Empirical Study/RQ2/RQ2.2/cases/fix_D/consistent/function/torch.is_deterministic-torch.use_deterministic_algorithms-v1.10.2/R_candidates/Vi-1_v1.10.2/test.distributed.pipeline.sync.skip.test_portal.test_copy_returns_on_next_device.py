@pytest.mark.skipif(not torch.cuda.is_available(), reason="cuda required")
def test_copy_returns_on_next_device():
    portal = Portal(torch.rand(1), tensor_life=1)

    prev_stream = default_stream(torch.device("cpu"))
    next_stream = default_stream(torch.device("cuda"))

    phony = torch.zeros(0, requires_grad=True)
    assert phony.device.type == "cpu"

    phony = portal.copy(prev_stream, next_stream, phony)
    assert phony.device.type == "cuda"
