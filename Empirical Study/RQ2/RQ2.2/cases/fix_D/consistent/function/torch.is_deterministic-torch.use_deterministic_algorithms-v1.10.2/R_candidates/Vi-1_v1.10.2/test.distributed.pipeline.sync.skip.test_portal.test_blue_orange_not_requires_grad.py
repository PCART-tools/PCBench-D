def test_blue_orange_not_requires_grad():
    tensor1 = torch.rand(1, requires_grad=True)
    tensor2 = torch.rand(1)

    # Same with: output = tensor1*2 + tensor2
    #
    #                +----------------------+
    #                |                      |
    # tensor2 -- PortalBlue -+      +- PortalOrange -+
    #                        |      |                |
    # tensor1 ------------ Join -- Fork --- Mul --- Add -- output
    #
    main = tensor1
    portal = Portal(tensor2, tensor_life=2)
    phony = portal.blue()
    main = join(main, phony)
    main, phony = fork(main)
    sub = portal.orange(phony)
    output = main * 2 + sub

    output.backward()

    assert torch.allclose(tensor1.grad, torch.tensor([2.0]))
    assert tensor2.grad is None
