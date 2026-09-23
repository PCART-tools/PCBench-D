def _should_pad_bench(
    match: Match,
    mat1: Tensor,
    mat2: Tensor,
    op: torch._ops.OpOverloadPacket,
    input: Optional[Tensor] = None,
) -> bool:
    do_bench = get_do_bench()

    m_padded_length = 0
    n_padded_length = 0
    with no_dispatch():
        if op is torch.ops.aten.mm or op is torch.ops.aten.addmm:
            m = mat1.shape[0]
            k = mat1.shape[1]
            n = mat2.shape[1]
            k_padded_length = get_padded_length(k, get_alignment_size(mat1))
            n_padded_length = get_padded_length(n, get_alignment_size(mat2))
            m_padded_length = get_padded_length(m, get_alignment_size(mat1))
        elif op is torch.ops.aten.bmm:
            m = mat1.shape[1]
            k = mat1.shape[2]
            n = mat2.shape[2]
            k_padded_length = get_padded_length(k, get_alignment_size(mat1))
            m_padded_length = get_padded_length(m, get_alignment_size(mat1))
            n_padded_length = get_padded_length(n, get_alignment_size(mat2))
        else:
            return False

        if m_padded_length == k_padded_length == n_padded_length == 0:
            return False

        def realize_symbols(
            ds: Union[torch.Size, tuple[torch.SymInt, ...]],
        ) -> list[int]:
            return [d if isinstance(d, int) else d.node.hint for d in ds]

        if any(
            dim == 0
            for dim in itertools.chain(
                realize_symbols(mat1.shape), realize_symbols(mat2.shape)
            )
        ):
            return False

        if torch._inductor.config.force_shape_pad:
            return True

        if (
            "pad_aten_mm_pass" in torch._inductor.config.post_grad_fusion_options
            and should_pad_mm_bf16(mat1.dtype, m, n, k)
        ):
            return True

        if not has_triton():
            return False

        if not is_mm_compute_bound(m, k, n, mat1.dtype):
            return False

        # We don't want to look up the cache for cases that are trivially false
        # since it does file io
        key = should_pad_bench_key(match, mat1, mat2, op, input)

        cached_pad = get_cached_should_pad(key)
        if cached_pad is not None:
            return cached_pad

        def realize_tensor(t):
            if isinstance(t, FakeTensor):
                size_hints = realize_symbols(t.size())
                stride_hint = realize_symbols(t.stride())
                real_size = (
                    sum((d - 1) * s for d, s in zip(size_hints, stride_hint)) + 1
                )
                real_t = torch.randn(real_size, dtype=t.dtype, device=t.device)
                return torch.as_strided(real_t, size_hints, stride_hint)
            else:
                return torch.randn_like(t)

        mat1 = realize_tensor(mat1)
        mat2 = realize_tensor(mat2)

        # since we key on whether or not the inputs can be memory planned, set cache for the
        # original time which is unaffected by whether or not the input can be planned
        ori_time_key = should_pad_bench_key(
            match, mat1, mat2, op, input, is_base_time_key=True
        )
        ori_time = get_cached_base_mm_benchmark_time(ori_time_key)
        if ori_time is None and op is torch.ops.aten.addmm and input is not None:
            # realize bias for addmm
            input = realize_tensor(input)

        mat1_pad = mat1
        mat2_pad = mat2

        is_bmm = op is torch.ops.aten.bmm

        mat1_pre_padded = should_exclude_padding_time(match, "mat1")
        fns = []
        if mat1_pre_padded and (m_padded_length or k_padded_length):
            mat1_pad = pad_mat1(
                mat1_pad,
                m_padded_length=m_padded_length,
                k_padded_length=k_padded_length,
                is_bmm=is_bmm,
            )

            def write_pad():
                if is_bmm:
                    mat1_pad[:, -m_padded_length:, -k_padded_length:].fill_(0)
                else:
                    mat1_pad[-m_padded_length:, -k_padded_length:].fill_(0)

            fns.append(write_pad)

        mat2_pre_padded = should_exclude_padding_time(match, "mat2")
        if mat2_pre_padded and (k_padded_length or n_padded_length):
            mat2_pad = pad_mat2(
                mat2_pad,
                k_padded_length=k_padded_length,
                n_padded_length=n_padded_length,
                is_bmm=is_bmm,
            )

            def write_pad():
                if is_bmm:
                    mat2_pad[:, -k_padded_length:, -n_padded_length:].fill_(0)
                else:
                    mat2_pad[-k_padded_length:, -n_padded_length:].fill_(0)

            fns.append(write_pad)

        if op is torch.ops.aten.addmm:
            input_pad = None
            if input is not None and input.is_cuda:
                input_pad = torch.randn_like(input)
            fns.append(
                lambda: pad_addmm(
                    input_pad,
                    mat1_pad,
                    mat2_pad,
                    m_padded_length,
                    k_padded_length,
                    n_padded_length,
                    mat1_pre_padded=mat1_pre_padded,
                    mat2_pre_padded=mat2_pre_padded,
                )
            )
        elif op is torch.ops.aten.mm:
            fns.append(
                lambda: pad_mm(
                    mat1_pad,
                    mat2_pad,
                    m_padded_length,
                    k_padded_length,
                    n_padded_length,
                    mat1_pre_padded=mat1_pre_padded,
                    mat2_pre_padded=mat2_pre_padded,
                )
            )
        else:
            fns.append(
                lambda: pad_bmm(
                    mat1_pad,
                    mat2_pad,
                    m_padded_length,
                    k_padded_length,
                    n_padded_length,
                    mat1_pre_padded=mat1_pre_padded,
                    mat2_pre_padded=mat2_pre_padded,
                )
            )

        def orig_bench_fn():
            if op is torch.ops.aten.bmm or op is torch.ops.aten.mm:
                op(mat1, mat2)
            else:
                op(input, mat1, mat2)

        def pad_bench_fn():
            for fn in fns:
                fn()

        if (
            torch._inductor.config.run_autoheuristic("pad_mm")
            and op is torch.ops.aten.mm
        ):
            ah_should_pad = run_autoheuristic(
                mat1,
                mat2,
                orig_bench_fn,
                pad_bench_fn,
                m_padded_length,
                k_padded_length,
                n_padded_length,
                do_bench,
                mat1_pre_padded,
                mat2_pre_padded,
                ori_time,
                ori_time_key,
                key,
            )
            if ah_should_pad is not None:
                return ah_should_pad

        if ori_time is None:
            ori_time = do_bench(orig_bench_fn)
            set_cached_base_mm_benchmark_time(ori_time_key, ori_time)

        pad_time = do_bench(pad_bench_fn)
        return should_pad(key, ori_time, pad_time)
