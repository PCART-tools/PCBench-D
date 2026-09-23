def _maybe_record_pointwise_barrier(
    func: object, proxy_mode: ProxyTorchDispatchMode
) -> None:
    """
    Records pointwise operators in user program (non decomposed) that were output in fp16/bf16
    """
    if proxy_mode.decomp_layers or not proxy_mode.emulate_precision_casts:
        return

    if (
        not isinstance(func, torch._ops.OpOverload)
        or torch.Tag.pointwise not in func.tags
    ):
        return

    last_node = next(iter(reversed(proxy_mode.tracer.graph.nodes)))
    t = last_node.meta.get("val")
    if not isinstance(t, torch.Tensor) or t.dtype not in (
        torch.bfloat16,
        torch.float16,
    ):
        return

    last_node.meta["low_precision_pointwise_barrier"] = True
