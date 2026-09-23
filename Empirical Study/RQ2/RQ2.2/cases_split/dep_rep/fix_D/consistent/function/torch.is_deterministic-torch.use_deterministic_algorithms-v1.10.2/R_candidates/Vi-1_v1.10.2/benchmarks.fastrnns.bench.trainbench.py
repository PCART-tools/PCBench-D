def trainbench(name, rnn_creator, nloops=100, warmup=10,
               seqLength=100, numLayers=1, inputSize=512, hiddenSize=512,
               miniBatch=64, device='cuda', seed=None):
    def train_batch(modeldef):
        # CUDA events for timing
        if device == 'cuda':
            timer_class = torch.cuda.Event
        else:
            timer_class = Event

        fwd_start_event = timer_class(enable_timing=True)
        fwd_end_event = timer_class(enable_timing=True)
        bwd_start_event = timer_class(enable_timing=True)
        bwd_end_event = timer_class(enable_timing=True)

        gc.collect()

        fwd_start_event.record()
        forward_output = modeldef.forward(*modeldef.inputs)
        fwd_end_event.record()

        # XXX: Use if need to print something
        # print(modeldef.forward.graph_for(*modeldef.inputs))

        if modeldef.backward_setup is not None:
            backward_input = modeldef.backward_setup(forward_output)
        else:
            backward_input = forward_output

        gc.collect()

        bwd_start_event.record()
        if modeldef.backward is not None:
            modeldef.backward(*backward_input)
        bwd_end_event.record()

        if modeldef.backward is not None:
            for param in modeldef.params:
                assert param.grad is not None
                param.grad.data.zero_()

        if device == 'cuda':
            torch.cuda.synchronize()

        fwd_time = fwd_start_event.elapsed_time(fwd_end_event)
        bwd_time = bwd_start_event.elapsed_time(bwd_end_event)
        return fwd_time, bwd_time

    creator_args = creator_args = {
        'seqLength': seqLength, 'numLayers': numLayers,
        'inputSize': inputSize, 'hiddenSize': hiddenSize,
        'miniBatch': miniBatch, 'device': device, 'seed': seed
    }

    modeldef = rnn_creator(**creator_args)

    [train_batch(modeldef) for _ in range(warmup)]

    results = [train_batch(modeldef) for _ in range(nloops)]
    fwd_times, bwd_times = zip(*results)

    fwd_times = torch.tensor(fwd_times)
    bwd_times = torch.tensor(bwd_times)
    return BenchResult(name=name,
                       avg_fwd=fwd_times.mean().item(),
                       std_fwd=fwd_times.std().item(),
                       info_fwd=fwd_times,
                       avg_bwd=bwd_times.mean().item(),
                       std_bwd=bwd_times.std().item(),
                       info_bwd=bwd_times)
