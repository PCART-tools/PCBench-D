@torch.inference_mode()
def benchmark(
    model,
    inputs,
    batch_iter: int,
    batch_size: int,
) -> None:
    """
    Run fx2trt lowering and benchmark the given model according to the
    specified benchmark configuration. Prints the benchmark result for each
    configuration at the end of the run.
    """

    model = model.cuda().eval()
    inputs = [x.cuda() for x in inputs]

    # benchmark base configuration
    conf = Configuration(batch_iter=batch_iter, batch_size=batch_size)

    configurations = [
        # Baseline
        replace(conf, name="CUDA Eager", trt=False),
        # FP32
        replace(conf, name="TRT FP32 Eager", trt=True, jit=False, fp16=False, accuracy_rtol=1e-3),
        # FP16
        replace(conf, name="TRT FP16 Eager", trt=True, jit=False, fp16=True, accuracy_rtol=1e-2),
    ]

    results = [
        run_configuration_benchmark(deepcopy(model), inputs, conf_) for conf_ in configurations
    ]

    for res in results:
        print(res.format())
