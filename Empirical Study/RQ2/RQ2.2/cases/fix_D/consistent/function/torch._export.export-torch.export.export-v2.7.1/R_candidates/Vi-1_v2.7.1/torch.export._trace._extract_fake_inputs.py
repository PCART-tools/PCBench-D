def _extract_fake_inputs(gm, args, kwargs):
    """
    Given a graph module, extract fakified input tensors from the metadata of
    its placeholders, and map them to the structure of given args and kwargs.
    Also return the fake mode used to fakify those inputs.
    """

    fake_inps: list[torch.Tensor] = []
    fake_vals: list[torch.Tensor] = []
    for node in gm.graph.nodes:
        if node.op == "placeholder" and "val" in node.meta:
            fake_val = node.meta["val"]
            if fake_val is not None and isinstance(fake_val, torch.Tensor):
                fake_inps.append(fake_val)
        elif "example_value" in node.meta:
            fake_val = node.meta["example_value"]
            if fake_val is not None and isinstance(fake_val, torch.Tensor):
                fake_vals.append(fake_val)

    if detected_fake_mode := detect_fake_mode(fake_inps + fake_vals):
        fake_mode = detected_fake_mode
    else:
        fake_mode = FakeTensorMode(shape_env=ShapeEnv(), export=True)

    count = 0

    def lookup_fake(x):
        nonlocal count
        val = fake_inps[count]
        count += 1
        return val

    fake_args = pytree.tree_map_only(torch.Tensor, lookup_fake, args)
    fake_kwargs = pytree.tree_map_only(torch.Tensor, lookup_fake, kwargs)

    return fake_args, fake_kwargs, fake_mode
