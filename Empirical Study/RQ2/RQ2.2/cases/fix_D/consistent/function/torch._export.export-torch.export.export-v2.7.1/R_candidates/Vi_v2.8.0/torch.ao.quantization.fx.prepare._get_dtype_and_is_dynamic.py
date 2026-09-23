def _get_dtype_and_is_dynamic(
    obs_or_fq: Optional[ObserverOrFakeQuantize],
) -> tuple[Optional[torch.dtype], bool]:
    """Given a constructor for observer or fake quant module, returns
    a Tuple of dtype and is_dynamic
    """
    # TODO: instead of instantiating the instance, we can use inspect to get the default args
    if obs_or_fq is None:
        return None, False
    else:
        return obs_or_fq.dtype, getattr(obs_or_fq, "is_dynamic", False)  # type: ignore[return-value]
