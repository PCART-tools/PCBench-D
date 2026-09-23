@compatibility(is_backward_compatible=False)
def fuse_by_partitions(
    gm: GraphModule,
    partitions: list[dict[Node, None]],
    prefix: str = "fused_",
    always_return_tuple: bool = False,
) -> GraphModule:
    for partition_id, partition in enumerate(partitions):
        sorted_nodes = topo_sort(list(partition))

        submodule_name = prefix + str(partition_id)
        sub_gm, orig_inputs, orig_outputs = fuse_as_graphmodule(
            gm,
            sorted_nodes,
            submodule_name,
            partition,
            always_return_tuple=always_return_tuple,
        )

        insert_subgm(gm, sub_gm, orig_inputs, orig_outputs)

        erase_nodes(gm, sorted_nodes)

    # topological sort original gm with newly created sub_gm
    legalize_graph(gm)

    return gm
