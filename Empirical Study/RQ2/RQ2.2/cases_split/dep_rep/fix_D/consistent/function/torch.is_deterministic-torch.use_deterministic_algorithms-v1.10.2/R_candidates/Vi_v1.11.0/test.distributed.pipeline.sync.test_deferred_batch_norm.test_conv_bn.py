def test_conv_bn():
    bn = nn.Sequential(nn.Conv2d(3, 3, 1), nn.BatchNorm2d(3))
    dbn = DeferredBatchNorm.convert_deferred_batch_norm(deepcopy(bn), chunks=CHUNKS)

    input = torch.rand(16, 3, 224, 224)
    input = tilt_dist(input)

    opt = optim.SGD(chain(bn.parameters(), dbn.parameters()), lr=0.1)

    # 1st step
    a = bn(input)
    b = chunked_forward(dbn, input)

    # Outputs are different. (per-mini-batch vs. per-micro-batch)
    assert not torch.allclose(a, b)

    a.sum().backward()
    b.sum().backward()
    opt.step()
    opt.zero_grad()

    # Conv layers are also trained differently because of their different outputs.
    assert not torch.allclose(bn[0].weight, dbn[0].weight)

    # But BNs track identical running stats.
    assert torch.allclose(bn[1].running_mean, dbn[1].running_mean, atol=1e-4)
    assert torch.allclose(bn[1].running_var, dbn[1].running_var, atol=1e3)

    # 2nd step
    a = bn(input)
    b = chunked_forward(dbn, input)
    a.sum().backward()
    b.sum().backward()

    # BNs can't track identical running stats due to the different conv layers.
    assert not torch.allclose(bn[1].running_mean, dbn[1].running_mean, atol=1e-4)
    assert not torch.allclose(bn[1].running_var, dbn[1].running_var, atol=1e3)
