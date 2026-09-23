@pytest.mark.parametrize("chunks", [1, 4])
@pytest.mark.parametrize("input_requires_grad", [True, False])
def test_transparency(chunks, input_requires_grad):
    bn = nn.BatchNorm2d(3)
    dbn = DeferredBatchNorm.convert_deferred_batch_norm(deepcopy(bn), chunks=chunks)

    input1 = torch.rand(16, 3, 224, 224)
    input1 = tilt_dist(input1)
    input2 = input1.clone()
    input1.requires_grad = input_requires_grad
    input2.requires_grad = input_requires_grad

    output1 = chunked_forward(bn, input1, chunks=chunks)
    output2 = chunked_forward(dbn, input2, chunks=chunks)

    assert torch.allclose(output1, output2, atol=1e-4)

    output1.mean().backward()
    output2.mean().backward()

    assert torch.allclose(bn.weight.grad, dbn.weight.grad, atol=1e-4)

    if input_requires_grad:
        assert input1.grad is not None
        assert input2.grad is not None
        assert torch.allclose(input1.grad, input2.grad, atol=1e-4)
