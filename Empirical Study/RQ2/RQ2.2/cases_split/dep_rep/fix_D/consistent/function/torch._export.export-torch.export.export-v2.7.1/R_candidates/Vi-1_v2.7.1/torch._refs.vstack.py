@out_wrapper()
def vstack(tensors: TensorSequenceType) -> TensorLikeType:
    torch._check(len(tensors) > 0, lambda: "vstack expects a non-empty TensorList")
    aligned_tensors = atleast_2d(*tensors)
    return cat(aligned_tensors, 0)
