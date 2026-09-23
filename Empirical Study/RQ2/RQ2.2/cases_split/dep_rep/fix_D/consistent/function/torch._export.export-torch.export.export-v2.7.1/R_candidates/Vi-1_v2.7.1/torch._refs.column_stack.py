@out_wrapper()
def column_stack(tensors: TensorSequenceType) -> TensorLikeType:
    aligned_tensors = tuple(
        x if x.ndim > 1 else x.reshape((x.numel(), 1)) for x in tensors
    )
    return cat(aligned_tensors, 1)
