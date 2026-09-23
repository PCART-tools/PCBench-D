def profile(rnns, sleep_between_seconds=1, nloops=5,
            internal_run=True,  # Unused, get rid of this TODO
            seqLength=100, numLayers=1, inputSize=512, hiddenSize=512,
            miniBatch=64, device='cuda', seed=None):
    params = dict(seqLength=seqLength, numLayers=numLayers,
                  inputSize=inputSize, hiddenSize=hiddenSize,
                  miniBatch=miniBatch, device=device, seed=seed)
    for name, creator, context in get_nn_runners(*rnns):
        with context():
            run_rnn(name, creator, nloops, **params)
            time.sleep(sleep_between_seconds)
