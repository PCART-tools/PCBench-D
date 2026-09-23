def run_configuration_benchmark(
    module,
    input,
    conf: Configuration,
) -> Result:
    """
    Runs `module` through lowering logic and benchmark the module before and
    after lowering.
    """
    print(f"=== Running benchmark for: {conf}", "green")
    time = -1.0

    if conf.fp16:
        module = module.half()
        input = [i.half() for i in input]

    if not conf.trt:
        # Run eager mode benchmark
        time = benchmark_torch_function(conf.batch_iter, lambda: module(*input))
    elif not conf.jit:
        # Run lowering eager mode benchmark
        lowered_module = lower_to_trt(module, input, max_batch_size=conf.batch_size, fp16_mode=conf.fp16)
        time = benchmark_torch_function(conf.batch_iter, lambda: lowered_module(*input))
    else:
        print("Lowering with JIT is not available!", "red")

    result = Result(
        module=module, input=input, conf=conf, time_sec=time
    )
    return result
