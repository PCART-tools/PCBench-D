def get_first_incompatible_cudagraph_node(
    gm: torch.fx.GraphModule,
) -> Optional[torch.fx.Node]:
    from torch.fx.experimental.symbolic_shapes import free_unbacked_symbols

    forbidden_set = OrderedSet(
        [
            "aten._fused_moving_avg_obs_fq_helper.default",
            "aten._fused_moving_avg_obs_fq_helper_functional.default",
            "fbgemm.dense_to_jagged.default",
            "fbgemm.jagged_to_padded_dense.default",
            "run_and_save_rng_state",
            "run_with_rng_state",
            "aten._local_scalar_dense",
            # Technically, it's not necessary to ban this, because an
            # assert_scalar with constant arguments can be validly run
            # with CUDA graphs, but the operator is also pointless with
            # constant arguments, so might as well ban
            "aten._assert_scalar",
        ]
    )
    if torch.are_deterministic_algorithms_enabled():
        forbidden_set.update(
            (
                "aten._unsafe_index_put.default",
                "aten._unsafe_masked_index_put_accumulate.default",
                "aten.index_put.default",
                "aten.index_put_.default",
                "aten.scatter.src",
                "aten.scatter.reduce",
                "aten.scatter.value_reduce",
                "aten.scatter_add_",
                "aten.scatter_add.default",
                "aten.scatter_reduce.two",
                "aten.scatter_reduce_.two",
                "aten.scatter_reduce.two_out",
            )
        )

    for node in gm.graph.nodes:
        if str(node.target) in forbidden_set:
            return node
        if (val := node.meta.get("val")) is not None and free_unbacked_symbols(val):
            return node
    return None
