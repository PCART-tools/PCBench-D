def _process_single_offline_gemm(untuned_gemm_line: str, gpu_id: int) -> None:
    r"""Process a single untuned GEMM."""

    deviceid = "cuda:" + str(gpu_id)

    dtype_dict = {
        "float": torch.float32,
        "double": torch.float64,
        "BFloat16": torch.bfloat16,
        "Half": torch.half,
        "c10::complex<double>": torch.complex128,
        "c10::complex<float>": torch.complex64,
        "Float8_e4m3fn": torch.float8_e4m3fn,
        "Float8_e5m2": torch.float8_e5m2,
        "Float8_e4m3fnuz": torch.float8_e4m3fnuz,
        "Float8_e5m2fnuz": torch.float8_e5m2fnuz,
    }

    untuned_gemm = untuned_gemm_line.strip().split(",")[:]

    underscore_count = untuned_gemm[0].count("_")

    # Initialize dtype to make linter happy
    dtype = None
    dtypeA = None
    dtypeB = None
    dtypeC = None

    if underscore_count == 2:
        [op_sig, data_type, layout] = untuned_gemm[0].split("_")
        transA = layout[0] == "T"
        transB = layout[1] == "T"
        dtype = dtype_dict.get(data_type)
    else:  # ScaledGEMM
        untuned_gemm_temp = untuned_gemm[0].split("_")
        # dtypeC = might not be FP8 type, keep track
        # of the the number of underscores
        count = untuned_gemm_temp.count("_")
        op_sig = untuned_gemm_temp[0]
        data_typeA = untuned_gemm_temp[1] + "_" + untuned_gemm_temp[2]
        data_typeB = untuned_gemm_temp[3] + "_" + untuned_gemm_temp[4]
        if count == 7:
            data_typeC = untuned_gemm_temp[5] + "_" + untuned_gemm_temp[6]
        else:
            data_typeC = untuned_gemm_temp[5]
        transA = untuned_gemm_temp[count][0] == "T"
        transB = untuned_gemm_temp[count][1] == "T"
        dtypeA = dtype_dict.get(data_typeA)
        dtypeB = dtype_dict.get(data_typeB)
        dtypeC = dtype_dict.get(data_typeC)

    untuned_gemm_temp = untuned_gemm[1].split("_")
    [n, m, k] = [int(g) for g in untuned_gemm_temp[1:4]]
    if op_sig == "GemmTunableOp":
        matA = (
            torch.rand(k, m, dtype=dtype, device=deviceid).t()
            if transB
            else torch.rand(m, k, dtype=dtype, device=deviceid)
        )
        matB = (
            torch.rand(n, k, dtype=dtype, device=deviceid).t()
            if transA
            else torch.rand(k, n, dtype=dtype, device=deviceid)
        )
        torch.mm(matA, matB)
    elif op_sig == "GemmStridedBatchedTunableOp":
        [b] = [int(g) for g in untuned_gemm_temp[5:6]]
        matA = (
            torch.rand(b, k, m, dtype=dtype, device=deviceid)
            if transB
            else torch.rand(b, m, k, dtype=dtype, device=deviceid)
        )
        matB = (
            torch.rand(b, n, k, dtype=dtype, device=deviceid)
            if transA
            else torch.rand(b, k, n, dtype=dtype, device=deviceid)
        )
        matA = matA.transpose(1, 2) if transB else matA
        matB = matB.transpose(1, 2) if transA else matB
        torch.bmm(matA, matB)
    elif op_sig == "ScaledGemmTunableOp":
        fillA = 0.25
        fillB = 0.75
        matA = (
            torch.full((k, m), fillA, dtype=dtypeA, device=deviceid).t()
            if transB
            else torch.full((m, k), fillA, dtype=dtypeA, device=deviceid)
        )
        matB = (
            torch.full((n, k), fillB, dtype=dtypeB, device=deviceid)
            if transA
            else torch.full((k, n), fillB, dtype=dtypeB, device=deviceid).t()
        )

        assert untuned_gemm_temp[8] == "rw"
        if untuned_gemm_temp[9] == "1":
            rowwise = True
        else:
            rowwise = False
        if rowwise:
            scaleA = torch.ones((matA.shape[0], 1), device=deviceid)
            scaleB = torch.ones((1, matB.shape[0]), device=deviceid)
        else:
            scaleA = torch.tensor(0.8, device=deviceid)
            scaleB = torch.tensor(0.9, device=deviceid)

        assert untuned_gemm_temp[10] == "bias"
        if untuned_gemm_temp[11] == "None":  # no bias vector
            torch._scaled_mm(
                matA, matB, scale_a=scaleA, scale_b=scaleB, out_dtype=dtypeC
            )
        else:  # bias vector present
            fillbias = 0.10
            bias_dtype = dtype_dict.get(untuned_gemm_temp[11])
            bias = (
                torch.full((n,), fillbias, dtype=bias_dtype, device=deviceid)
                if transA
                else torch.full((m,), fillbias, dtype=bias_dtype, device=deviceid)
            )
            torch._scaled_mm(
                matA, matB, scale_a=scaleA, scale_b=scaleB, out_dtype=dtypeC, bias=bias
            )

    elif op_sig == "GemmAndBiasTunableOp":
        # y = x*A^T + b
        assert transA != transB

        X = (
            torch.rand(k, m, dtype=dtype, device=deviceid).t()
            if transB
            else torch.rand(m, k, dtype=dtype, device=deviceid)
        )
        matA = (
            torch.rand(n, k, dtype=dtype, device=deviceid)
            if transA
            else torch.rand(k, n, dtype=dtype, device=deviceid).t()
        )
        bias = (
            torch.rand(n, dtype=dtype, device=deviceid)
            if transA
            else torch.rand(m, dtype=dtype, device=deviceid)
        )
        torch.nn.functional.linear(X, matA, bias)
    else:
        warnings.warn(f"error: unknown op {op_sig}")
