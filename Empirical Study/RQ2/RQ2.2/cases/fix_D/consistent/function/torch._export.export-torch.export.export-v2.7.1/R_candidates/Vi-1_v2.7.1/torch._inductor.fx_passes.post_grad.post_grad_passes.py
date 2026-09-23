def post_grad_passes(gm: torch.fx.GraphModule, is_inference: bool):
    """
    Passes that run on after grad.  This is called once on the forwards
    graph and once on the backwards graph.

    The IR here has been normalized and functionalized.
    """
    GraphTransformObserver = functools.partial(
        torch.fx.passes.graph_transform_observer.GraphTransformObserver,
        subsystem="post_grad_passes",
    )

    if not torch._dynamo.config.skip_fsdp_hooks:
        remove_fsdp2_unsharded_param_graph_input_usage(gm.graph)

    if config.dce:
        # has some issues with mutation in inference mode
        gm.graph.eliminate_dead_code()

    if is_inference and config.reorder_for_locality:
        GraphTransformObserver(gm, "reorder_for_locality").apply_graph_pass(
            reorder_for_locality
        )

    fake_tensor_updater = FakeTensorUpdater(gm.graph)

    if post_grad_custom_pre_pass := config.post_grad_custom_pre_pass:
        GraphTransformObserver(gm, "post_grad_custom_pre_pass").apply_graph_pass(
            post_grad_custom_pre_pass
        )

    if (
        config.cpp.enable_grouped_gemm_template
        and config.max_autotune
        and "CPP" in config.max_autotune_gemm_backends
        and torch._C._has_mkldnn
    ):
        from .mkldnn_fusion import grouped_gemm_pass

        grouped_gemm_pass(gm.graph)

    if config.pattern_matcher:
        lazy_init()
        trace_structured(
            "artifact",
            metadata_fn=lambda: {
                "name": "before_recompile_post_grad",
                "encoding": "string",
            },
            payload_fn=lambda: gm.print_readable(
                print_output=False, include_stride=True, include_device=True
            ),
        )
        GraphTransformObserver(gm, "post_grad_custom_pre_pass").apply_graph_pass(
            functools.partial(group_batch_fusion_passes, pre_grad=False)
        )
        GraphTransformObserver(gm, "remove_noop_ops").apply_graph_pass(remove_noop_ops)
        GraphTransformObserver(gm, "remove_assert_ops").apply_graph_pass(
            remove_assert_ops
        )
        for i, patterns in enumerate(pass_patterns):
            GraphTransformObserver(gm, f"pass_pattern_{i}").apply_graph_pass(
                patterns.apply
            )
        for pass_name in config.post_grad_fusion_options:
            # skip all patterns for group batch fusions
            if pass_name in POST_GRAD_FUSIONS:
                continue
            pattern_matcher_pass = POST_GRAD_PATTERNS[pass_name]
            inductor_before_change = save_inductor_dict(
                [pattern_matcher_pass.pass_name]
            )
            GraphTransformObserver(gm, pass_name).apply_graph_pass(
                pattern_matcher_pass.apply
            )
            if not is_same_dict(counters["inductor"], inductor_before_change):
                trace_structured(
                    "artifact",
                    metadata_fn=lambda: {
                        "name": f"{pattern_matcher_pass.pass_name}_post_grad",
                        "encoding": "string",
                    },
                    payload_fn=lambda: gm.print_readable(
                        print_output=False, include_stride=True, include_device=True
                    ),
                )
        if config.b2b_gemm_pass:
            B2B_GEMM_PASS.apply(gm.graph)  # type: ignore[arg-type]

    if config._micro_pipeline_tp:
        micro_pipeline_tp_pass(gm.graph)

    if config._fuse_ddp_communication:
        GraphTransformObserver(gm, "fuse_ddp_communication").apply_graph_pass(
            lambda graph: fuse_ddp_communication(
                graph,
                config._fuse_ddp_communication_passes,
                config._fuse_ddp_bucket_size,
            )
        )

    if post_grad_custom_post_pass := config.post_grad_custom_post_pass:
        GraphTransformObserver(gm, "post_grad_custom_post_pass").apply_graph_pass(
            post_grad_custom_post_pass
        )

    GraphTransformObserver(gm, "stable_sort").apply_graph_pass(stable_topological_sort)

    GraphTransformObserver(gm, "move_constructors_to_cuda").apply_graph_pass(
        move_constructors_to_gpu
    )

    fake_tensor_updater.incremental_update()

    # Keep these last, since they introduces mutation. Look at
    # ./fx_passes/README.md for a discussion of mutation invariants.
    GraphTransformObserver(gm, "reinplace_inplaceable_ops").apply_graph_pass(
        reinplace_inplaceable_ops
    )
    GraphTransformObserver(
        gm, "decompose_triton_kernel_wrapper_functional"
    ).apply_graph_pass(decompose_triton_kernel_wrapper_functional)
    GraphTransformObserver(gm, "decompose_auto_functionalized").apply_graph_pass(
        decompose_auto_functionalized
    )
    GraphTransformObserver(gm, "reinplace_fsdp_all_gather").apply_graph_pass(
        comms.reinplace_fsdp_all_gather
    )

    gm.recompile()
    trace_structured(
        "artifact",
        metadata_fn=lambda: {
            "name": "after_recompile_post_grad",
            "encoding": "string",
        },
        payload_fn=lambda: gm.print_readable(
            print_output=False, include_stride=True, include_device=True
        ),
    )
    gm.graph.lint()
