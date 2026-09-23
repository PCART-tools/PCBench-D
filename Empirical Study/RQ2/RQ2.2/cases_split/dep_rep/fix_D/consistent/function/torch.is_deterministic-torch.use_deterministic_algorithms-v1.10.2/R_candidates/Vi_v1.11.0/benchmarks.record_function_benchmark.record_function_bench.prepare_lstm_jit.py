def prepare_lstm_jit(bench_args):
    model_def = lstm_creator(
        script=True,
        seqLength=bench_args.lstmSeqLength,
        numLayers=bench_args.lstmNumLayers,
        inputSize=bench_args.lstmInputSize,
        hiddenSize=bench_args.lstmHiddenSize,
        miniBatch=bench_args.lstmMiniBatch,
        device='cpu')
    return model_def.inputs, model_def.forward
