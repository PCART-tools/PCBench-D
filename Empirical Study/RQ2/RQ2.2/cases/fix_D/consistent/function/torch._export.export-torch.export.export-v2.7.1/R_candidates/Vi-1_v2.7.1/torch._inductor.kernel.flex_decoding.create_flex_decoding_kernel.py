def create_flex_decoding_kernel(*args, **kwargs):
    from .flex_attention import set_head_dim_values

    (
        query,
        key,
        value,
        block_mask,
        scale,
        kernel_options,
        score_mod_subgraph,
        mask_mod_subgraph,
        score_mod_other_buffers,
        mask_mod_other_buffers,
    ) = args
    (
        _,  # q_length
        _,  # kv_length
        kv_num_blocks,
        kv_indices,
        full_kv_num_blocks,  # full_kv_num_blocks,
        full_kv_indices,  # full_kv_indices,
        _,  # q_num_blocks
        _,  # q_indices
        _,  # full_q_num_blocks,
        _,  # full_q_indices,
        _,  # SPARSE_Q_BLOCK_SIZE,
        SPARSE_KV_BLOCK_SIZE,
        _,
    ) = block_mask

    Bq, Hq, seq_len_q, qk_head_dim = query.get_size()
    Bkv, Hkv, seq_len_kv, v_head_dim = value.get_size()

    assert V.graph.sizevars.evaluate_expr(sympy.Eq(Bq, Bkv) | sympy.Eq(Bkv, 1)), (
        f"Bq and Bkv must broadcastable. Got Bq={Bq} and Bkv={Bkv}"
    )

    B = Bq
    kernel_options = dict(kernel_options)
    # Mark symbols in custom kernel options as static shapes and add guards.
    kernel_options = {
        k: V.graph.sizevars.evaluate_static_shape(v)
        if isinstance(v, sympy.Symbol)
        else v
        for k, v in kernel_options.items()
    }

    # TODO: Fix flex decoding non-divisible case!
    if seq_len_q % 128 != 0 or seq_len_kv % 128 != 0:
        kernel_options.setdefault("IS_DIVISIBLE", False)
    else:
        kernel_options.setdefault("IS_DIVISIBLE", True)

    # Calculate GQA head sharing
    gqa_shared_heads = Hq // Hkv
    if not is_power_of_2(gqa_shared_heads):
        raise ValueError(
            "Number of shared query heads sharing the same KV head must be power of 2. "
        )
    kernel_options.setdefault("GQA_SHARED_HEADS", gqa_shared_heads)

    # Determine if there are "full" blocks where we only need to apply score_mod, and can skip mask_mod
    has_full_blocks = full_kv_num_blocks is not None
    kernel_options.setdefault("HAS_FULL_BLOCKS", has_full_blocks)
    if not has_full_blocks:
        # Create a plackeholder full block list in case it is empty
        full_kv_num_blocks, full_kv_indices = (
            empty(0, device=query.get_device()) for _ in range(2)
        )

    (
        query,
        key,
        value,
        kv_num_blocks,
        kv_indices,
        full_kv_num_blocks,
        full_kv_indices,
    ) = maybe_realize(
        [
            query,
            key,
            value,
            kv_num_blocks,
            kv_indices,
            full_kv_num_blocks,
            full_kv_indices,
        ]
    )
    score_mod_other_buffers = maybe_realize(score_mod_other_buffers)
    mask_mod_other_buffers = maybe_realize(mask_mod_other_buffers)

    choices: list[Any] = []
    configs: list[tuple[int, int, int]] = []
    configs.append(_get_decoding_default_config(key))
    # Note: max_autotune is not supported yet. Causes error in lowering the dynamic shape in reduction ops.
    if config.max_autotune:
        configs += [
            (64, 2, 2),
            (32, 2, 3),
            (128, 2, 3),
        ]

        # Use num_stages=1 on ROCm to avoid shmem limitation
        if torch.version.hip:
            configs = [(c[0], c[1], 1) for c in configs]

    # TODO: fix autotuning.

    kernel_options.setdefault("SM_SCALE", scale)
    kernel_options.setdefault("SPLIT_KV", get_split_k(B, Hkv, seq_len_kv))
    MAX_SPLIT_KV = kernel_options["SPLIT_KV"]

    # create config dependent intermediate buffers
    buf_ACC_shape = [B, MAX_SPLIT_KV, Hq, seq_len_q, v_head_dim]
    buf_ML_shape = buf_ACC_shape[:-1]
    buf_M = empty_strided(
        buf_ML_shape,
        None,
        dtype=torch.float32,  # The rowmax is always stored in fp32 regardless of the input dtype
        device=query.get_device(),
    )
    buf_L = empty_strided(
        buf_ML_shape,
        None,
        dtype=torch.float32,  # The intermediate sumexp is always stored in fp32 regardless of the input dtype
        device=query.get_device(),
    )

    layout_acc = FixedLayout(
        query.get_device(),
        torch.float32,
        buf_ACC_shape,
        FlexibleLayout.contiguous_strides(buf_ACC_shape),
    )

    set_head_dim_values(kernel_options, qk_head_dim, v_head_dim, V.graph.sizevars)

    kernel_options.setdefault(
        "BLOCK_M",
        (
            # m
            # if V.graph.sizevars.evaluate_expr(sympy.Lt(query.get_size()[-2], 0))
            # else  # Always use a BLOCK_M > 16 before Triton fix https://github.com/triton-lang/triton/pull/4061 is in pin
            max(
                next_power_of_2(
                    V.graph.sizevars.size_hint(
                        seq_len_q,
                        fallback=torch._inductor.config.unbacked_symint_fallback,  # type: ignore[arg-type]
                    )
                    * gqa_shared_heads
                ),
                16,
            )
        ),
    )

    query = ir.ExternKernel.realize_input(query)
    stride_b, stride_hq, stride_seq_len_q, stride_qk_head_dim = query.get_stride()

    # Reshape query for GQA: [B, Hq, Mq, D] -> [B, Hkv, G, Mq, D]
    gqa_query_shape = (B, Hkv, gqa_shared_heads, seq_len_q, qk_head_dim)
    gqa_query_stride = (
        stride_b,
        stride_hq * gqa_shared_heads,
        stride_hq,
        stride_seq_len_q,
        stride_qk_head_dim,
    )
    query = lowerings[aten.as_strided](query, gqa_query_shape, gqa_query_stride)

    V.graph.sizevars.guard_leq(
        seq_len_q * gqa_shared_heads, sympy.Integer(kernel_options["BLOCK_M"])
    )

    kernel_options.setdefault(
        "SAFE_M_BOUNDARY",
        ((seq_len_q * gqa_shared_heads) % kernel_options["BLOCK_M"]) == 0,
    )
    # TODO: This feels sketchy
    kernel_options.setdefault("SAFE_N_BOUNDARY", True)
    # Mark SPARSE_KV_BLOCK_SIZE as static shapes and add guards.
    SPARSE_KV_BLOCK_SIZE = V.graph.sizevars.evaluate_static_shape(SPARSE_KV_BLOCK_SIZE)

    original_kernel_options = kernel_options.copy()
    # Note, we don't need to pass in the captured buffers explicitly
    # because they're implicitly added by the score_mod function
    # We do need to explicitly pass it in for autotuning though.
    for BLOCK_N, num_warps, num_stages in configs:
        if SPARSE_KV_BLOCK_SIZE % BLOCK_N != 0:
            continue

        cur_kernel_options = original_kernel_options.copy()
        # Remove prefix for forward kernels options and delete backward kernel options.
        for k in list(cur_kernel_options.keys()):
            if k.startswith("fwd_"):
                v = cur_kernel_options.pop(k)
                cur_kernel_options[k[4:]] = v
            if k.startswith("bwd_"):
                cur_kernel_options.pop(k)
        # Performance tuning
        cur_kernel_options.setdefault("BLOCK_N", BLOCK_N)
        cur_kernel_options.setdefault("SPARSE_KV_BLOCK_SIZE", SPARSE_KV_BLOCK_SIZE)
        cur_kernel_options.setdefault("num_warps", num_warps)
        cur_kernel_options.setdefault("num_stages", num_stages)

        flex_decoding_template.maybe_append_choice(
            choices=choices,
            input_nodes=[
                query,
                key,
                value,
                buf_M,
                buf_L,
                kv_num_blocks,
                kv_indices,
                full_kv_num_blocks,
                full_kv_indices,
            ],
            layout=layout_acc,
            subgraphs=[
                score_mod_subgraph,
                mask_mod_subgraph,
            ],
            mutated_inputs=[buf_M, buf_L],
            call_sizes=query.get_size(),
            **cur_kernel_options,
        )

    inputs_for_flex_decoding = (
        [
            query,
            key,
            value,
            buf_M,
            buf_L,
            kv_num_blocks,
            kv_indices,
            full_kv_num_blocks,
            full_kv_indices,
        ]
        + list(score_mod_other_buffers)
        + list(mask_mod_other_buffers)
    )

    input_gen_fns = {
        5: create_num_blocks_fake_generator(kv_indices),
        6: create_indices_fake,
        7: create_num_blocks_fake_generator(full_kv_indices),
        8: create_indices_fake,
    }

    buf_ACC = autotune_select_algorithm(
        "flex_decoding",
        choices,
        inputs_for_flex_decoding,
        layout_acc,
        input_gen_fns=input_gen_fns,
    )

    # Reduction

    g_M = lowerings[aten.max](buf_M, dim=1, keepdim=True)[0]
    # See [Note] Handle fully masked out rows:
    # g_M Is the global max among split kv blocks.
    masked_rows = lowerings[aten.eq](g_M, -float("inf"))
    adj_M = lowerings[aten.sub](buf_M, g_M)
    adj_M = lowerings[aten.where](masked_rows, 0, adj_M)
    alpha = lowerings[aten.exp2](adj_M)

    buf_L = lowerings[aten.mul](buf_L, alpha)
    g_L = lowerings[aten.sum](buf_L, axis=1)
    masked_rows_squeezed = lowerings[aten.squeeze](masked_rows, dim=1)
    g_L = lowerings[aten.where](masked_rows_squeezed, 1.0, g_L)
    logsumexp = lowerings[aten.log2](g_L)
    logsumexp = lowerings[aten.add](logsumexp, lowerings[aten.squeeze](g_M, dim=1))

    alpha_unseq = lowerings[aten.unsqueeze](alpha, 4)
    buf_ACC = lowerings[aten.mul](buf_ACC, alpha_unseq)
    output = lowerings[aten.sum](buf_ACC, axis=1)
    L_unseq = lowerings[aten.unsqueeze](g_L, 3)
    output = lowerings[aten.div](output, L_unseq)
    output = lowerings[prims.convert_element_type](output, query.get_dtype())

    return (
        output,
        logsumexp,
    )
