def should_pad(key: str, ori_time: float, pad_time: float) -> bool:
    multiplier = 1.1
    # Shape padding introduces additional memory ops. Based on microbenchmarks, 1.1x represents a reasonable
    # tradeoff between performance improvement from shape padding and overhead from additional memory ops
    # TODO: Build a learned model which would be better than this heuristic
    if "shape_padding_multiplier" in torch._inductor.config.post_grad_fusion_options:
        multiplier = torch._inductor.config.post_grad_fusion_options[
            "shape_padding_multiplier"
        ].get("value", 1.1)
        counters["inductor"]["shape_padding_multiplier"] += 1
    should_pad = _skip_do_bench_times or ori_time > pad_time * multiplier
    set_cached_should_pad(key, should_pad)
    return should_pad
