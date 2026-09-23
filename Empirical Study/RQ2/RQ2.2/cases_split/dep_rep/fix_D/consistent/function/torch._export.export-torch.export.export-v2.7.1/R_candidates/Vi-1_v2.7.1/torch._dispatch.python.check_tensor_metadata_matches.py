def check_tensor_metadata_matches(nv, rv, desc):
    assert callable(desc)
    assert nv.size() == rv.size(), f"{desc()}: sizes {nv.size()} != {rv.size()}"
    assert nv.dtype == rv.dtype, f"{desc()}: dtype {nv.dtype} != {rv.dtype}"
    same_strides, idx = torch._prims_common.check_significant_strides(
        nv, rv, only_cuda=False
    )
    assert same_strides, (
        f"{desc()}: strides {nv.stride()} != {rv.stride()} (mismatch at index {idx})"
    )
