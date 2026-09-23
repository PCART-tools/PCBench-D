def test_rnns(experim_creator, control_creator, check_grad=True, verbose=False,
              seqLength=100, numLayers=1, inputSize=512, hiddenSize=512,
              miniBatch=64, device='cuda', seed=17):
    creator_args = dict(seqLength=seqLength, numLayers=numLayers,
                        inputSize=inputSize, hiddenSize=hiddenSize,
                        miniBatch=miniBatch, device=device, seed=seed)

    print("Setting up...")
    control = control_creator(**creator_args)
    experim = experim_creator(**creator_args)

    # Precondition
    assertEqual(experim.inputs, control.inputs)
    assertEqual(experim.params, control.params)

    print("Checking outputs...")
    control_outputs = control.forward(*control.inputs)
    experim_outputs = experim.forward(*experim.inputs)
    assertEqual(experim_outputs, control_outputs)

    print("Checking grads...")
    assert control.backward_setup is not None
    assert experim.backward_setup is not None
    assert control.backward is not None
    assert experim.backward is not None
    control_backward_inputs = control.backward_setup(control_outputs, seed)
    experim_backward_inputs = experim.backward_setup(experim_outputs, seed)

    control.backward(*control_backward_inputs)
    experim.backward(*experim_backward_inputs)

    control_grads = [p.grad for p in control.params]
    experim_grads = [p.grad for p in experim.params]
    assertEqual(experim_grads, control_grads)

    if verbose:
        print(experim.forward.graph_for(*experim.inputs))
    print('')
