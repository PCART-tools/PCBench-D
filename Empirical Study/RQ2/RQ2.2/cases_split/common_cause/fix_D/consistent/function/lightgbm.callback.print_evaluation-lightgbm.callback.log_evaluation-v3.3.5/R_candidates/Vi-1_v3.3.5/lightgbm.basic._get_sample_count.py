def _get_sample_count(total_nrow: int, params: str):
    sample_cnt = ctypes.c_int(0)
    _safe_call(_LIB.LGBM_GetSampleCount(
        ctypes.c_int32(total_nrow),
        c_str(params),
        ctypes.byref(sample_cnt),
    ))
    return sample_cnt.value
