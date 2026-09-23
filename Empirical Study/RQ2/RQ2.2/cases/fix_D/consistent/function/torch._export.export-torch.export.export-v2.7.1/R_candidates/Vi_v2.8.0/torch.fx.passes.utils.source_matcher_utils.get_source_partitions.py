@compatibility(is_backward_compatible=False)  # type: ignore[misc]
def get_source_partitions(
    graph: Graph,
    wanted_sources: list[Any],
    filter_fn: Optional[Callable[[Node], bool]] = None,
) -> dict[Any, list[SourcePartition]]:
    """
    Args:
        graph: The graph we want to partition
        wanted_sources: List of sources of nodes that were decomposed from this
            source. This can be a function (ex. torch.nn.functional.linear) or a
            leaf module type (ex. torch.nn.Linear).

    Returns:
        Dictionary mapping sources that were given to a list of SourcePartitions
        that correspond to the list of nodes that were decomposed from the given
        source.
    """
    modules: dict[type, dict[str, list[Node]]] = {}

    for node in graph.nodes:
        # The metadata source_fn should contain a tuple of a unique name for the
        # source, and the source function if the node is decomposed from a
        # function, or the type of module if the node is decomposed from a leaf
        # module

        # TODO: Bypass "torch_fn" when "source_fn_stack" because now "torch_fn" can
        # be different from "source_fn_stack", for example for the add_ node
        # decomposed from batch norm. We should remove the check on "source_fn_stack"
        # after we fix "torch_fn". T199561090
        if (source_fn_st := node.meta.get("source_fn_stack", None)) is None and (
            torch_fn := node.meta.get("torch_fn", None)
        ) is not None:
            node_fqn, source_fn = torch_fn
            source_fn_name = source_fn.split(".")[1]
            if source_fn_name in wanted_sources:
                diff_modules = modules.setdefault(source_fn_name, {})
                partition = diff_modules.setdefault(node_fqn, [])
                partition.append(node)

        if (source_fn_st := node.meta.get("source_fn_stack", None)) is not None:
            source_fn = source_fn_st[-1]
            if source_fn[1] in wanted_sources:
                diff_modules = modules.setdefault(source_fn[1], {})
                partition = diff_modules.setdefault(source_fn[0], [])
                partition.append(node)

    def make_partition(nodes: list[Node], module_type: type) -> SourcePartition:
        input_nodes = set()
        output_nodes = set()
        params = set()
        for node in nodes:
            for arg in node.args:
                if isinstance(arg, Node) and arg not in nodes and arg.op != "get_attr":
                    input_nodes.add(arg)

            if node.op == "get_attr":
                params.add(node)
                # get_attr nodes won't be output nodes
                continue

            for user in node.users.keys():
                if user not in nodes:
                    output_nodes.add(node)

        return SourcePartition(
            nodes,
            module_type,
            list(input_nodes),
            list(output_nodes),
            list(params),  # type: ignore[arg-type]
        )

    ret: dict[type[Any], list[SourcePartition]] = {}

    if filter_fn:
        # for each partition, we apply filter_fn to filter out all partitions that doesn't satisfy the
        # filter condition
        filtered_modules = {}
        for tp, name_to_partition in modules.items():
            filtered_name_to_partition = {
                name: partition
                for name, partition in name_to_partition.items()
                if all(map(filter_fn, partition))
            }
            filtered_modules[tp] = filtered_name_to_partition
        modules = filtered_modules

    for k, v in modules.items():
        ret[k] = [make_partition(partition, k) for partition in v.values()]

    return ret
