@register_lowering(
    torch.ops.higher_order.flex_attention_backward, type_promotion_kind=None
)
def flex_attention_backward(*args, **kwargs):
    (
        query,
        key,
        value,
        out,
        logsumexp,
        grad_out,
        grad_logsumexp,
        fw_graph,
        joint_graph,
        block_mask,
        scale,
        kernel_options,
        score_mod_other_buffers,
        mask_mod_other_buffers,
    ) = args
    (
        _,  # q_length
        _,  # kv_length
        kv_num_blocks,
        kv_indices,
        full_kv_num_blocks,
        full_kv_indices,
        q_num_blocks,
        q_indices,
        full_q_num_blocks,
        full_q_indices,
        SPARSE_Q_BLOCK_SIZE,
        SPARSE_KV_BLOCK_SIZE,
        mask_graph,
    ) = block_mask

    (
        query,
        key,
        value,
        grad_out,
        kv_num_blocks,
        kv_indices,
        full_kv_num_blocks,
        full_kv_indices,
        q_num_blocks,
        q_indices,
        full_q_num_blocks,
        full_q_indices,
    ) = maybe_realize(
        [
            query,
            key,
            value,
            grad_out,
            kv_num_blocks,
            kv_indices,
            full_kv_num_blocks,
            full_kv_indices,
            q_num_blocks,
            q_indices,
            full_q_num_blocks,
            full_q_indices,
        ]
    )

    device = query.get_device()
    dtype = query.get_dtype()
    Bq, Hq, seq_len_q, qk_head_dim = query.get_size()
    Bkv, Hkv, seq_len_kv, v_head_dim = value.get_size()

    assert V.graph.sizevars.evaluate_expr(sympy.Eq(Bq, Bkv) | sympy.Eq(Bkv, 1)), (
        f"Bq and Bkv must broadcastable. Got Bq={Bq} and Bkv={Bkv}"
    )

    kernel_options = dict(kernel_options)
    # Mark symbols in custom kernel options as static shapes and add guards.
    kernel_options = {
        k: V.graph.sizevars.evaluate_static_shape(v)
        if isinstance(v, sympy.Symbol)
        else v
        for k, v in kernel_options.items()
    }
    kernel_options.setdefault("FLOAT32_PRECISION", get_float32_precision())
    if seq_len_q % 128 != 0 or seq_len_kv % 128 != 0:
        kernel_options.setdefault("IS_DIVISIBLE", False)
    else:
        kernel_options.setdefault("IS_DIVISIBLE", True)

    fwd_placeholder_inps = [
        create_placeholder(name, dtype, device)
        for name, dtype in [
            ("score", dtype),
            ("b", torch.int32),
            ("h", torch.int32),
            ("m", torch.int32),
            ("n", torch.int32),
        ]
    ]
    fw_subgraph_buffer = build_subgraph_buffer(
        fwd_placeholder_inps + list(score_mod_other_buffers), fw_graph
    )

    joint_placeholder_inps = fwd_placeholder_inps + [
        create_placeholder("grad_score_mod", dtype, device)
    ]
    # Sometimes we have weird unused nodes here
    joint_graph.graph_module.graph.eliminate_dead_code()

    # It is hard to raise nice errors for some joint graphs during subgraph lowering
    # This lets us do some checks before attempting to lower
    validate_joint_graph(joint_graph.graph_module.graph)

    all_joint_outputs = build_subgraph_buffer(
        joint_placeholder_inps + list(score_mod_other_buffers),
        joint_graph,
    )

    joint_outputs = process_joint_outputs(
        all_joint_outputs, len(joint_placeholder_inps)
    )

    mask_graph_placeholder_inps = [
        create_placeholder(name, dtype, query.get_device())
        for name, dtype in [
            ("b", torch.int32),
            ("h", torch.int32),
            ("m", torch.int32),
            ("n", torch.int32),
        ]
    ]
    mask_graph_buffer = build_subgraph_buffer(
        mask_graph_placeholder_inps + list(mask_mod_other_buffers), mask_graph
    )

    mask_graph_buffer = mask_graph_buffer

    # Construct layout with stride order matching K
    key_size = [Bq, Hkv, seq_len_kv, qk_head_dim]
    key_strides = infer_dense_strides(key_size, key.get_stride())

    layout_broadcasted_k = FixedLayout(
        key.get_device(),
        key.get_dtype(),
        key_size,
        stride=[sympy.sympify(s) for s in key_strides],
    )

    # Create delta which will is needed for the bwd's kernel
    grad_lse_exp2 = lowerings[aten.mul](grad_logsumexp, 1 / math.log(2))
    mul_delta = lowerings[aten.mul](out, grad_out)
    delta = lowerings[aten.sum](mul_delta, axis=-1)
    delta = lowerings[aten.sub](delta, grad_lse_exp2)
    delta = ExternKernel.require_contiguous(delta)

    grad_lse_exp2, delta = maybe_realize([grad_lse_exp2, delta])

    # # see NOTE:[TritonTemplates with multiple outputs]
    query_size = [Bq, Hq, seq_len_q, qk_head_dim]
    grad_query_strides = infer_dense_strides(query_size, query.get_stride())
    grad_query = empty_strided(
        query_size,
        stride=[sympy.sympify(s) for s in grad_query_strides],
        dtype=query.get_dtype(),
        device=query.get_device(),
    )

    # Construct output layout with stride order matching value
    value_size = [Bq, Hkv, seq_len_kv, v_head_dim]
    value_strides = infer_dense_strides(value_size, value.get_stride())

    broadcasted_grad_value = empty_strided(
        value_size,
        stride=[sympy.sympify(s) for s in value_strides],
        dtype=value.get_dtype(),
        device=value.get_device(),
    )

    kernel_options.setdefault("SM_SCALE", scale)

    # Determine GQA factor
    gqa_shared_heads = Hq // Hkv
    kernel_options.setdefault("GQA_SHARED_HEADS", gqa_shared_heads)

    # Inside of Triton kernel, only apply partial masking if partial blocks are computed.
    # full_kv_num_blocks is torch.zeros([1, 1, 1]) if partial blocks are not computed.
    has_full_blocks = full_kv_num_blocks is not None
    kernel_options.setdefault("HAS_FULL_BLOCKS", has_full_blocks)
    if not has_full_blocks:
        full_kv_num_blocks, full_kv_indices, full_q_num_blocks, full_q_indices = (
            empty(0, device=query.get_device()) for _ in range(4)
        )

    set_head_dim_values(kernel_options, qk_head_dim, v_head_dim, V.graph.sizevars)

    SPARSE_Q_BLOCK_SIZE = V.graph.sizevars.evaluate_static_shape(SPARSE_Q_BLOCK_SIZE)
    SPARSE_KV_BLOCK_SIZE = V.graph.sizevars.evaluate_static_shape(SPARSE_KV_BLOCK_SIZE)

    choices: list[Any] = []
    configs: list[tuple[int, int, int, int]] = []
    configs.append(_get_default_config_bwd(query))
    if config.max_autotune:
        num_stages_list = [1, 3, 4, 5] if torch.version.hip is None else [1]
        configs.extend(
            [
                (BLOCK1, BLOCK2, w, s)
                for BLOCK1 in [32, 64]
                for BLOCK2 in [32, 64, 128]
                for w in ([4, 8] if BLOCK1 >= 128 or BLOCK2 >= 128 else [4])
                for s in num_stages_list
                if BLOCK2 % BLOCK1 == 0
            ]
        )
    original_kernel_options = kernel_options.copy()
    for BLOCK1, BLOCK2, num_warps, num_stages in configs:
        if (
            SPARSE_KV_BLOCK_SIZE % BLOCK1 != 0
            or SPARSE_Q_BLOCK_SIZE % BLOCK1 != 0
            or SPARSE_KV_BLOCK_SIZE % BLOCK2 != 0
            or SPARSE_Q_BLOCK_SIZE % BLOCK2 != 0
        ):
            continue

        # Performance tuning
        # Triton heuristics
        cur_kernel_options = original_kernel_options.copy()
        # Remove prefix for backward kernels options and delete forward kernel options.
        for k in list(cur_kernel_options.keys()):
            if k.startswith("bwd_"):
                v = cur_kernel_options.pop(k)
                cur_kernel_options[k[4:]] = v
            if k.startswith("fwd_"):
                cur_kernel_options.pop(k)
        cur_kernel_options.setdefault("num_warps", num_warps)
        cur_kernel_options.setdefault("num_stages", num_stages)

        cur_kernel_options.setdefault("BLOCK_M1", BLOCK1)
        cur_kernel_options.setdefault("BLOCK_N1", BLOCK2)
        cur_kernel_options.setdefault("BLOCK_M2", BLOCK2)
        cur_kernel_options.setdefault("BLOCK_N2", BLOCK1)
        # Blocksparse options
        cur_kernel_options.setdefault("SPARSE_Q_BLOCK_SIZE", SPARSE_Q_BLOCK_SIZE)
        cur_kernel_options.setdefault("SPARSE_KV_BLOCK_SIZE", SPARSE_KV_BLOCK_SIZE)

        flex_attention_backward_template.maybe_append_choice(
            choices=choices,
            input_nodes=[
                query,
                key,
                value,
                logsumexp,
                delta,
                grad_out,
                grad_query,
                broadcasted_grad_value,
                kv_num_blocks,
                kv_indices,
                q_num_blocks,
                q_indices,
                full_kv_num_blocks,
                full_kv_indices,
                full_q_num_blocks,
                full_q_indices,
            ],
            layout=layout_broadcasted_k,  # We use store_output only for grad_key
            subgraphs=[
                fw_subgraph_buffer,
                joint_outputs.grad_input,
                mask_graph_buffer,
                joint_outputs.captured_grads_compute,
            ],
            mutated_inputs=[
                grad_query,
                broadcasted_grad_value,
                *joint_outputs.mutated_grads,
            ],
            call_sizes=query.get_size() + key.get_size()[1:3],
            **cur_kernel_options,
        )
    inputs_for_autotuning = (
        [
            query,
            key,
            value,
            logsumexp,
            delta,
            grad_out,
            grad_query,
            broadcasted_grad_value,
            kv_num_blocks,
            kv_indices,
            q_num_blocks,
            q_indices,
            full_kv_num_blocks,
            full_kv_indices,
            full_q_num_blocks,
            full_q_indices,
        ]
        + list(score_mod_other_buffers)
        + list(mask_mod_other_buffers)
        + joint_outputs.mutated_grads
    )
    input_gen_fns = {
        8: create_num_blocks_fake_generator(kv_indices),  # kv_num_blocks
        9: create_indices_fake,
        10: create_num_blocks_fake_generator(q_indices),  # q_num_blocks
        11: create_indices_fake,
        12: create_num_blocks_fake_generator(full_kv_indices),  # full_kv_num_blocks
        13: create_indices_fake,
        14: create_num_blocks_fake_generator(full_q_indices),  # full_q_num_blocks
        15: create_indices_fake,
    }

    broadcasted_grad_key = autotune_select_algorithm(
        "flex_attention_backward",
        choices,
        inputs_for_autotuning,
        layout_broadcasted_k,
        input_gen_fns=input_gen_fns,
    )  # [Bq, Hkv, seq_len_kv, k_head_dim]

    if V.graph.sizevars.evaluate_expr(sympy.Eq(Bq, Bkv)):
        grad_key = broadcasted_grad_key
        grad_value = broadcasted_grad_value
    else:
        assert V.graph.sizevars.evaluate_expr(sympy.Gt(Bq, 1) & sympy.Eq(Bkv, 1)), (
            f"Bq and Bkv must broadcastable. "
            f"Got Bq={V.graph.sizevars.evaluate_expr(Bq)} "
            f"and Bkv={V.graph.sizevars.evaluate_expr(Bkv)}"
        )
        grad_key = lowerings[aten.sum](broadcasted_grad_key, axis=0, keepdims=True)
        grad_value = lowerings[aten.sum](broadcasted_grad_value, axis=0, keepdims=True)

    return (grad_query, grad_key, grad_value, tuple(joint_outputs.captured_grads))
