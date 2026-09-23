def get_do_bench() -> Callable[[Callable[[], Any]], float]:
    with dynamo_timed("pad_mm_benchmark_get_do_bench"):
        return functools.partial(
            torch._inductor.runtime.benchmarking.benchmarker.benchmark_gpu,
            warmup=5,
        )
