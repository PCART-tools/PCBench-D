def run_rnn(name, rnn_creator, nloops=5,
            seqLength=100, numLayers=1, inputSize=512, hiddenSize=512,
            miniBatch=64, device='cuda', seed=None):
    def run_iter(modeldef):
        # Forward
        forward_output = modeldef.forward(*modeldef.inputs)

        # "loss computation" and backward
        if modeldef.backward_setup is not None:
            backward_input = modeldef.backward_setup(forward_output)
        else:
            backward_input = forward_output
        if modeldef.backward is not None:
            modeldef.backward(*backward_input)

        # "Update" parameters
        if modeldef.backward is not None:
            for param in modeldef.params:
                param.grad.data.zero_()
        torch.cuda.synchronize()

    assert device == 'cuda'
    creator_args = dict(seqLength=seqLength, numLayers=numLayers,
                        inputSize=inputSize, hiddenSize=hiddenSize,
                        miniBatch=miniBatch, device=device, seed=seed)
    modeldef = rnn_creator(**creator_args)

    [run_iter(modeldef) for _ in range(nloops)]
