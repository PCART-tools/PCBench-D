def _resolve_name_collision(mod: GraphModule, gm: GraphModule) -> None:
    """
    In aot_export_module (make_fx), we create get_attr nodes with name prefix
    "_tensor_constant" and "_torchbind_obj". See Tracer.create_arg() in
    torch/fx/_symbolic_trace.py

    However, this might result in name collision if the original mod already
    has a different buffer with the same name.

    We resolve this potential name collision here by changing the target name
    with a new number post fix.
    """

    existing_keys = OrderedSet(
        [name for name, val in mod.named_parameters(remove_duplicate=False)]
    )
    existing_keys.update(
        OrderedSet([name for name, val in mod.named_buffers(remove_duplicate=False)])
    )

    def find_smallest_i(graph: fx.Graph, prefix: str) -> int:
        i = 0
        for node in graph.nodes:
            if node.op == "get_attr" and node.target.startswith(prefix):
                if len(node.target) > len(prefix):
                    post_fix = node.target.split(prefix)[-1]
                    if post_fix.isdigit():
                        i = max(i, int(post_fix))
        for key in existing_keys:
            if key.startswith(prefix):
                if len(key) > len(prefix):
                    post_fix = key.split(prefix)[-1]
                    if post_fix.isdigit():
                        i = max(i, int(post_fix))
        return i + 1

    for node in gm.graph.nodes:
        if node.op == "get_attr":
            target_name = node.target
            if not target_name.startswith(
                "_tensor_constant"
            ) and not target_name.startswith("_torchbind_obj"):
                continue

            if not hasattr(mod, target_name):
                continue
            gm_target = attrgetter(target_name)(gm)
            model_target = attrgetter(target_name)(mod)
            if (
                torch.equal(gm_target, model_target)
                and gm_target.dtype == model_target.dtype
            ):
                continue

            prefix = (
                "_tensor_constant"
                if target_name.startswith("_tensor_constant")
                else "_torchbind_obj"
            )
            new_id = find_smallest_i(gm.graph, prefix)
            new_target_name = f"{prefix}{new_id}"
            node.target = new_target_name
            setattr(gm, new_target_name, gm_target)
            existing_keys.add(new_target_name)
