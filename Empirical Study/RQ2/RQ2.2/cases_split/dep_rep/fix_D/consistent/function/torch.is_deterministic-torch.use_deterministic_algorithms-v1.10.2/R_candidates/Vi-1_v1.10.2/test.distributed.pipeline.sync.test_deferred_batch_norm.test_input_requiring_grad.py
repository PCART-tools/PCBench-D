def test_input_requiring_grad():
    dbn = DeferredBatchNorm(3, chunks=CHUNKS)

    input = torch.rand(16, 3, 224, 224)
    input = tilt_dist(input)
    input.requires_grad = True

    chunked_forward(dbn, input)

    assert not dbn.sum.requires_grad
    assert dbn.sum.grad_fn is None
