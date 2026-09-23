    def mps_ops_grad_modifier(ops: Sequence[OpInfo]) -> Sequence[OpInfo]:
        XFAILLIST_GRAD = {
            # Unimplemented ops
            "_segment_reduce": [torch.float16, torch.float32],
            "_chunk_cat": [torch.float16, torch.float32],
            "_upsample_bilinear2d_aa": None,  # `_upsample_bilinear2d_aa_backward_out` not implemented for MPS
            "_upsample_bicubic2d_aa": None,  # `_upsample_bilinear2d_aa_backward_out` not implemented for MPS
            "sparse.mmreduce": [torch.float32],  # csr not supported
            "unique_consecutive": [torch.float16, torch.float32],
            "scalar_tensor": [torch.float16, torch.float32],
            "cdist": [torch.float32],
            "masked.scatter": [torch.float16, torch.float32],
            "index_fill": [torch.float16, torch.float32],  # missing `aten::_unique`.
            "linalg.solve": [torch.float16, torch.float32],  # missing `aten::lu_solve`.
            "linalg.solve_ex": [
                torch.float16,
                torch.float32,
            ],  # missing `aten::lu_solve`.
            "linalg.tensorsolve": [
                torch.float16,
                torch.float32,
            ],  # missing `aten::lu_solve`.
            "linalg.det": [torch.float16, torch.float32],  # missing aten::lu_solve.out
            "linalg.slogdet": [
                torch.float16,
                torch.float32,
            ],  # missing aten::lu_solve.out
            "logdet": [torch.float16, torch.float32],  # missing aten::lu_solve.out
            "aminmax": [torch.float32, torch.float16],
            "special.i1": [torch.float16],  # "i1_backward" not implemented for 'Half'
            "special.i1e": [torch.float16],  # "i1e_backward" not implemented for 'Half'
            # Correctness issues
            "atanh": [torch.float32],
            # Random output
            "exponential": [torch.float16, torch.float32],
            # CPU errors
            # derivative for zeta is not implemented
            "special.zeta": None,
            # derivative for aten::nextafter is not implemented on CPU
            "nextafter": None,
            # derivative for aten::floor_divide is not implemented on CPU
            "floor_divide": [torch.float16, torch.float32],
            # derivative for aten::narrow_copy is not implemented on CPU
            "narrow_copy": [torch.float16, torch.float32],
            # derivative for aten::_histogramdd_from_bin_cts is not implemented on CPU
            "histogramdd": [torch.float16, torch.float32],
            # derivative for aten::histogram is not implemented
            "histogram": [torch.float16, torch.float32],
            # 'bool' object is not iterable
            "allclose": [torch.float16, torch.float32],
            "equal": [torch.float16, torch.float32],
            # 'float' object is not iterable
            "item": [torch.float16, torch.float32],
            # "smooth_l1_backward_cpu_out" not implemented for 'Half'
            "nn.functional.smooth_l1_loss": [torch.float16],
            # cpu error: grad requires non-empty inputs
            "randn": [torch.float16, torch.float32],
            "signal.windows.bartlett": [torch.float32],
            "signal.windows.blackman": [torch.float32],
            "signal.windows.cosine": [torch.float32],
            "signal.windows.exponential": [torch.float32],
            "signal.windows.gaussian": [torch.float32],
            "signal.windows.general_cosine": [torch.float32],
            "signal.windows.general_hamming": [torch.float32],
            "signal.windows.hamming": [torch.float32],
            "signal.windows.hann": [torch.float32],
            "signal.windows.kaiser": [torch.float32],
            "signal.windows.nuttall": [torch.float32],
            "eye": [torch.float16, torch.float32],
            # round not working properly for float16
            "round": [torch.float16],
            # topk fails with duplicate indices
            "topk": [torch.float16],
        }

        MACOS_BEFORE_13_3_XFAILLIST_GRAD = {
            # Failures due to precision issues (may be fast-math). These has been fixed in MacOS 14
            "masked.softmin": [torch.float32, torch.float16],
            "masked.softmax": [torch.float32, torch.float16],
            "masked.log_softmax": [torch.float32, torch.float16],
            "atanh": [torch.float16],
            "triangular_solve": [torch.float32],
            # Unsupported Border padding mode, forward pass success as fallback to cpu
            "grid_sampler_2d": [torch.float32, torch.float16, torch.bfloat16],
            # Same issue as `argsort` and `sort` with duplicate elements (undefined behaviour).
            # Forward pass is passing since `msort` doesn't return the indices, just the values, which match the CPU.
            # On the backward pass for `sort` both are used (values and indices), thus resulting in a issmatch between CPU and MPS.
            # Running `msort` with stable `sort` passes.
            "msort": [torch.float16],
        }

        SKIPLIST_GRAD = {
            "nn.functional.pairwise_distance": [torch.float16],
            # failed assertion `destination datatype must be fp32'
            "nn.functional.conv1d": [torch.float16],
            "nn.functional.conv2d": [torch.float16],
            "nn.functional.conv3d": [torch.float16],
            "nn.functional.conv_transpose1d": [torch.float16],
            "nn.functional.conv_transpose2d": [torch.float16],
            "nn.functional.conv_transpose3d": [torch.float16],
        }

        MACOS_13_3_XFAILLIST_GRAD = {
            # Same issue as `argsort` and `sort` with duplicate elements (undefined behaviour).
            # Forward pass is passing since `msort` doesn't return the indices, just the values, which match the CPU.
            # On the backward pass for `sort` both are used (values and indices), thus resulting in a issmatch between CPU and MPS.
            # Running `msort` with stable `sort` passes.
            "msort": [torch.float16],
        }

        ON_MPS_XFAILLIST = {
            # Failures due to lack of implementation of downstream functions on MPS backend
            # TODO: remove these once downstream function 'aten::_linalg_svd.U' have been implemented
            "linalg.matrix_rank": None,
            # Exception: Caused by sample input at index 3 on MPS
            "nn.functional.conv3d": [torch.float32],
        }

        def addDecorator(op: OpInfo, d: DecorateInfo) -> None:
            op.decorators = op.decorators + (d,)

        for op in ops:
            key = op.name + op.variant_test_name
            if key in XFAILLIST_GRAD:
                addDecorator(
                    op,
                    DecorateInfo(unittest.expectedFailure, dtypes=XFAILLIST_GRAD[key]),
                )

            if key in SKIPLIST_GRAD:
                addDecorator(op, DecorateInfo(unittest.skip, dtypes=SKIPLIST_GRAD[key]))

            if key in ON_MPS_XFAILLIST:
                addDecorator(
                    op,
                    DecorateInfo(
                        unittest.expectedFailure, dtypes=ON_MPS_XFAILLIST[key]
                    ),
                )

            if key in MACOS_BEFORE_13_3_XFAILLIST_GRAD and (
                torch.backends.mps.is_macos13_or_newer() and MACOS_VERSION < 13.3
            ):
                addDecorator(
                    op,
                    DecorateInfo(
                        unittest.expectedFailure,
                        dtypes=MACOS_BEFORE_13_3_XFAILLIST_GRAD[key],
                    ),
                )

            if key in MACOS_13_3_XFAILLIST_GRAD and (MACOS_VERSION >= 13.3):
                addDecorator(
                    op,
                    DecorateInfo(
                        unittest.expectedFailure, dtypes=MACOS_13_3_XFAILLIST_GRAD[key]
                    ),
                )
        return ops
