def benchmark_pytorch_model(model, inputs, training=False, warmup_iters=3,
                            main_iters=10, verbose=False):
    '''
        Run the model several times, and measure the execution time.
        Return the execution time per iteration (millisecond).
    '''
    for _i in range(warmup_iters):
        model(*inputs)
    total_pytorch_time = 0.0
    for _i in range(main_iters):
        ts = time.time()
        model(*inputs)
        te = time.time()
        total_pytorch_time += te - ts
    log.info("The PyTorch model execution time per iter is {} milliseconds, "
             "{} iters per second.".format(total_pytorch_time / main_iters * 1000,
                                           main_iters / total_pytorch_time))
    return total_pytorch_time * 1000 / main_iters
