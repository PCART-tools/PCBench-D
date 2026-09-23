def prepare_softmax_extra_check(match):
    """
    We only have triton online softmax kernels currently.
    """
    return (
        config.online_softmax
        and match.kwargs["x"].meta["val"].device.type == "cuda"
        and config.cuda_backend == "triton"
    )
