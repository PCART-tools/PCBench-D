def _broadcast_rank0_decision(
    joint_graph: torch.fx.Graph, saved_values: list[torch.fx.Node]
):
    # use the same policy across different GPUs
    from torch._subclasses.fake_tensor import unset_fake_temporarily

    def has_collectives(joint_graph):
        for node in joint_graph.nodes:
            if isinstance(
                node.target, torch._ops.OpOverload
            ) and node.target.namespace in {"_c10d_functional", "c10d_functional"}:
                return True
        return False

    def has_same_nodes(joint_graph):
        # proxy to check if the graph is the same across different GPUs.
        # We only consider the name and order of nodes. A more robust way
        # would be to check the hash of the whole graph (disregarding input shapes),
        # this is is a reasonable first-order approximation.
        node_str = "/".join(x.name for x in joint_graph.nodes)
        inputs = hashlib.sha256(node_str.encode("utf-8")).hexdigest()
        all_inputs = [None for _ in range(torch.distributed.get_world_size())]
        with no_dispatch(), unset_fake_temporarily():
            # TODO: maybe use a different process group?
            torch.distributed.all_gather_object(all_inputs, inputs)
        return all(all_inputs[0] == x for x in all_inputs)

    if (
        torch.distributed.is_available()
        and torch.distributed.is_initialized()
        and torch.distributed.get_world_size() > 1
        and has_collectives(joint_graph)
        and has_same_nodes(joint_graph)
    ):
        with no_dispatch(), unset_fake_temporarily():
            objects = [[x.name for x in saved_values]]
            # TODO: maybe use a different process group for this
            torch.distributed.broadcast_object_list(objects, src=0)
            saved_values_names = objects[0]
            name_to_node = get_name_to_node(joint_graph)
            saved_values = [name_to_node[n] for n in saved_values_names]
    return saved_values
