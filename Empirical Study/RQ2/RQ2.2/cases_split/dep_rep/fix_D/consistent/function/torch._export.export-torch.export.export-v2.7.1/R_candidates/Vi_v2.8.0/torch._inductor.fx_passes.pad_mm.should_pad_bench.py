def should_pad_bench(*args: Any, **kwargs: Any) -> bool:
    with dynamo_timed(
        "pad_mm_benchmark",
        log_pt2_compile_event=False,
        dynamo_compile_column_us="compile_time_autotune_time_us",
    ):
        return _should_pad_bench(*args, **kwargs)
