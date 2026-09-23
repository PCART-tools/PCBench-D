def set_example_value(node, example_value):
    # NB: example_value is a bit of a misnomer, because this is always a fake
    # tensor of some sort.  Furthermore, these example values serve as the
    # runtime state of Dynamo tracing, which means if metadata mutation
    # occurs, the example_value gets directly updated (so you can't rely on
    # this to accurately reflect what the state of the value was at the time
    # the program was traced).
    node.meta["example_value"] = example_value
    shape_env = TracingContext.get().fake_mode.shape_env
    if (
        symbol_to_path
        := torch.fx.experimental.symbolic_shapes.compute_unbacked_bindings(
            shape_env, example_value
        )
    ):
        node.meta["unbacked_bindings"] = symbol_to_path
