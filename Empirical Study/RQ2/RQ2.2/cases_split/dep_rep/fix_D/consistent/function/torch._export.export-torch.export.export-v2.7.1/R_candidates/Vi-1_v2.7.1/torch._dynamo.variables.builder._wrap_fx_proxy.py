def _wrap_fx_proxy(
    target_cls, tx, proxy, example_value=None, subclass_type=None, **options
):
    from ..symbolic_convert import InstructionTranslatorBase

    assert isinstance(tx, InstructionTranslatorBase)
    if "guards" in options and options["guards"] is not None:
        tx.output.guards.update(options["guards"])

    assert "example_value" not in proxy.node.meta, f"{proxy.node.meta['example_value']}"

    # See NOTE: [Deferring tensor pack/unpack hooks until runtime]
    with torch._dynamo.utils._disable_saved_tensors_hooks_during_tracing():
        # with preserve_rng_state():
        # only allow_non_graph_fake in this instance because we handle the non-fake
        # cases properly below.
        example_value = get_fake_value(proxy.node, tx, allow_non_graph_fake=True)

    return handle_traced_output(
        example_value, tx, proxy, options, subclass_type, target_cls
    )
