def median(
    a: ArrayLike,
    axis=None,
    out: Optional[OutArray] = None,
    overwrite_input=False,
    keepdims: KeepDims = False,
):
    return quantile(
        a,
        torch.as_tensor(0.5),
        axis=axis,
        overwrite_input=overwrite_input,
        out=out,
        keepdims=keepdims,
    )
