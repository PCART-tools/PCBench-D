def should_fallback_to_aten(choices: list[ChoiceCaller]) -> bool:
    if len(choices) == 0 and not use_aten_gemm_kernels():
        if inductor_config.autotune_fallback_to_aten:
            log.warning(
                "No choices for GEMM, using ATen backend as fallback. "
                "This behavior is being deprecated. Please add include Aten in max_autotune_gemm_backends."
            )
            return True
        else:
            log.warning(
                "No choices for GEMM, chose not to fallback to ATen backend. "
                "To temporarily change this behavior, set autotune_fallback_to_aten to True "
                "via TORCHINDUCTOR_AUTOTUNE_FALLBACK_TO_ATEN=1, but this knob is being deprecated. "
                "The long term fix is to include Aten in max_autotune_gemm_backends."
            )
            return False
    return False
