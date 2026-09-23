@register_debug_backend  # type: ignore[arg-type]
def dynamo_accuracy_minifier_backend(gm, example_inputs, compiler_name):
    from functorch.compile import minifier

    compiler_fn = lookup_backend(compiler_name)

    # Set the eval mode to remove randomness.
    gm.eval()

    # Check Accuracy
    if _accuracy_fails(gm, example_inputs, compiler_fn):
        log.warning("Accuracy failed for the TorchDynamo produced graph")
        dump_state_fn = functools.partial(
            dump_backend_state, compiler_name=compiler_name, check_accuracy=True
        )
        fails_fn = functools.partial(
            _accuracy_fails,
            compiler_fn=compiler_fn,
        )
        dump_state_fn(fx.GraphModule(gm, copy.deepcopy(gm.graph)), example_inputs)
        minifier(
            gm,
            example_inputs,
            module_fails=fails_fn,
            dump_state=dump_state_fn,
        )
    else:
        log.error("Input graph does not fail accuracy testing")
    return gm
