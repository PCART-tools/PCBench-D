    def _unary_fusion_pattern(unary_fusion, call_fn, users, lowp_dtype):
        # only insert to_dtype if lowp_dtype is True
        computation_call = (
            _to_float(call_fn(), users=users) if lowp_dtype else call_fn(users=users)
        )
        out = unary_fusion(computation_call)
        if lowp_dtype == torch.bfloat16:
            return _to_bf16(out)
        elif lowp_dtype == torch.float16:
            return _to_fp16(out)
        else:
            return out
