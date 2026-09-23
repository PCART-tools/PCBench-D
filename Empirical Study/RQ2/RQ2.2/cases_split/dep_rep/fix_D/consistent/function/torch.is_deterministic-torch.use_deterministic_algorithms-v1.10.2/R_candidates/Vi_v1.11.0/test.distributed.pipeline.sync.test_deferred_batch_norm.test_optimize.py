def test_optimize():
    bn = nn.BatchNorm2d(3)
    dbn = DeferredBatchNorm.convert_deferred_batch_norm(deepcopy(bn), chunks=CHUNKS)

    opt = optim.SGD(chain(bn.parameters(), dbn.parameters()), lr=1.0)

    for i in range(5):
        input = torch.rand(16, 3, 224, 224)
        input = tilt_dist(input)

        # train
        y = bn(input)
        a = y.sum()
        a.backward()

        y = chunked_forward(dbn, input)
        b = y.sum()
        b.backward()

        opt.step()

        # eval
        bn.eval()
        dbn.eval()

        with torch.no_grad():
            assert torch.allclose(bn(input), dbn(input), atol=1e-1 * (10 ** i))
