@out_wrapper()
def dstack(tensors: TensorSequenceType) -> TensorLikeType:
    torch._check(len(tensors) > 0, lambda: "dstack expects a non-empty TensorList")
    aligned_tensors = atleast_3d(*tensors)
    return cat(aligned_tensors, 2)
