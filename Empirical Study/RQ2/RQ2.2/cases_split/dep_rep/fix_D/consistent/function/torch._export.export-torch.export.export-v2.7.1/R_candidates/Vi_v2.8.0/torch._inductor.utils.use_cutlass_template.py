def use_cutlass_template(layout: Layout, m: int, n: int, k: int) -> bool:
    from .virtualized import V

    gemm_size = V.graph.sizevars.size_hint(m * n * k, fallback=-1)
    if gemm_size <= 0 or gemm_size < config.cuda.cutlass_backend_min_gemm_size:
        return False
    from .codegen.cuda.cutlass_utils import try_import_cutlass

    # Do not use cutlass template on ROCm
    if torch.version.hip:
        return False

    # output dtype
    # FP32 not supported: https://github.com/pytorch/pytorch/issues/145952
    layout_dtypes = [torch.float16, torch.bfloat16, torch.int32]
    res = (
        _use_template_for_gpu(layout, layout_dtypes)
        and (config.max_autotune or config.max_autotune_gemm)
        and _use_autotune_backend("CUTLASS")
    )

    if res:
        if not try_import_cutlass():
            log.warning(
                "Failed to import CUTLASS lib. Please check whether "
                "_inductor.config.cuda.cutlass_dir is set correctly. "
                "Skipping CUTLASS backend for now."
            )
            return False
    return res
