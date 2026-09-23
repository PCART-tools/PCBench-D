def set_missing_meta_vals(gm, flat_args, num_params_buffers):
    # Sets missing metadata to address two problems:
    # 1. aot_export adds symint metadata for placeholders with int values; since
    #    these become specialized, we replace such metadata with the original values.
    # 2. any tensor attributes that are not params / buffers, i.e., are constants
    #    need to have their metadata set before lifting them because it is needed
    #    for computing the exported program's signature.
    index = 0
    fake_mode = detect_fake_mode(flat_args)
    for node in gm.graph.nodes:
        if node.op == "placeholder":
            if index >= num_params_buffers:
                user_arg = flat_args[index - num_params_buffers]
                if not isinstance(user_arg, torch.Tensor):
                    node.meta["val"] = user_arg
            index += 1
        if node.op == "get_attr":
            val = _get_attr(gm, node.target)
            if isinstance(val, torch.Tensor):
                assert "val" not in node.meta, (
                    f"Found attribute {node.target} that has already been fakified "
                    "but not yet lifted as an input. This should be impossible because "
                    "(1) we should have already fakified AND lifted params/buffers "
                    "(2) we should have NOT yet fakified OR lifted tensor constants. "
                )
                node.meta["val"] = fake_mode.from_tensor(val, static_shapes=True)
