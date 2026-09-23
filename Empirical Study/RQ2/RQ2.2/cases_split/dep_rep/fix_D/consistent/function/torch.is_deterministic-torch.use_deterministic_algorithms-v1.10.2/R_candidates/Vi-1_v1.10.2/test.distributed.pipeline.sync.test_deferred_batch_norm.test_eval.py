def test_eval():
    bn = nn.BatchNorm2d(3)
    dbn = DeferredBatchNorm.convert_deferred_batch_norm(deepcopy(bn), chunks=CHUNKS)

    input = torch.rand(16, 3, 224, 224)
    input = tilt_dist(input)

    bn(input)
    chunked_forward(dbn, input)

    bn.eval()
    dbn.eval()

    assert torch.allclose(bn(input), dbn(input), atol=1e-4)
