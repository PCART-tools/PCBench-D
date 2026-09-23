def create_micro_gemm(
    name,
    m,
    n,
    k,
    input_dtype,
    input2_dtype,
    output_dtype=None,
    compute_dtype=None,
    alpha=1,
    num_threads=-1,
    use_ref=True,
    q_group_size=None,
) -> Optional[CppMicroGemm]:
    """
    Based on the provided info, try to find the config of the micro-kernel that would
    deliver the best performance in terms of lower latency for this case.
    """

    def create_from_config(cls, config: CppMicroGemmConfig):
        return cls(
            name,
            config.input_dtype,
            config.input2_dtype,
            config.output_dtype,
            config.compute_dtype,
            config.register_blocking,
            alpha,
        )

    def skip_amx_kernel_for_woq(config, dynamic_M, micro_gemm_cls):
        # For WoQ GEMM, AMX micro-kernel may not perform well if m is small.
        # Exception: for dynamic shapes, we consider using the AMX micro-kernel.
        if (
            dynamic_M
            or input_dtype != torch.bfloat16
            or input2_dtype not in [torch.int8, torch.uint8]
        ):
            return False
        # For WOQ INT8, use AMX for m >= block_m
        # For WOQ INT4, use AMX for m >= 5
        block_m, *_ = config.register_blocking
        is_woq_int4 = micro_gemm_cls == CppMicroGemmWoQInt4Amx
        m_threshold = 5 if is_woq_int4 else block_m
        return m < m_threshold

    assert isinstance(n, int) or n.is_number, n
    assert isinstance(k, int) or k.is_number, k
    from ..utils import has_free_symbols

    dynamic_M = has_free_symbols((m,))
    m = V.graph.sizevars.size_hint(m, fallback=1) if dynamic_M else m
    assert isinstance(m, int) or m.is_number, m
    if output_dtype is None:
        output_dtype = input_dtype
    if compute_dtype is None:
        compute_dtype = output_dtype
    if num_threads < 0:
        num_threads = parallel_num_threads()
    vec_isa = pick_vec_isa()
    matched_configs = []
    for cls, configs in micro_gemm_configs.items():
        for config in configs:
            if not issubclass(vec_isa.__class__, config.vec_isa_cls):
                continue
            if (
                config.input_dtype == input_dtype
                and config.compute_dtype == compute_dtype
                and config.input2_dtype == input2_dtype
                and config.output_dtype == output_dtype
                # The output_dtype here is the output dtype of the micro-kernel.
                # In some cases, the actual output dtype of the op for which the micro-kernel
                # is being created would be same as that of the activation, but the micro-kernels
                # compute output in Float/int32, which is converted in the GEMM template. This is
                # subject to change in the future.
            ):
                if config.extra_check is not None and not config.extra_check(
                    config,
                    m,
                    n,
                    k,
                    alpha,
                    num_threads,
                    dynamic_M=dynamic_M,
                    q_group_size=q_group_size,
                ):
                    continue
                block_m, block_n, block_k = config.register_blocking
                if config.vec_isa_cls == VecAMX and skip_amx_kernel_for_woq(
                    config, dynamic_M, cls
                ):
                    continue
                # Criteria on the ranking of configurations
                # 1. ISA: AMX > VEC
                # 2. Dividable by block sizes (block_m, block_n, block_k)
                # 3. Number of mxn blocks is large enough to occupy all the threads
                # 4. Register blocks are larger
                isa_score = 0
                if config.vec_isa_cls == VecAMX:
                    isa_score += 1
                dividable_score = 0
                if m % block_m == 0:
                    dividable_score += 1
                if n % block_n == 0:
                    dividable_score += 1
                if k % block_k == 0:
                    dividable_score += 1
                occupancy_score = 0
                n_blocks = (n + block_n - 1) // block_n
                total_mxn_blocks = n_blocks * ((m + block_m - 1) // block_m)
                if n_blocks >= num_threads:
                    occupancy_score += 1
                if total_mxn_blocks >= num_threads:
                    occupancy_score += 1
                register_bytes = (
                    block_m * block_n * config.compute_dtype.itemsize
                    + (block_m * block_k + block_k * block_n)
                    * config.input_dtype.itemsize
                )
                matched_configs.append(
                    (
                        (isa_score, dividable_score, occupancy_score, register_bytes),
                        cls,
                        config,
                    )
                )
    if len(matched_configs) == 0:
        if use_ref:
            return CppMicroGemmRef(
                name, input_dtype, input2_dtype, output_dtype, compute_dtype, alpha
            )
        else:
            return None
    # TODO(jgong5): allow autotuning on choices of configs
    return create_from_config(*max(matched_configs, key=operator.itemgetter(0))[1:])
