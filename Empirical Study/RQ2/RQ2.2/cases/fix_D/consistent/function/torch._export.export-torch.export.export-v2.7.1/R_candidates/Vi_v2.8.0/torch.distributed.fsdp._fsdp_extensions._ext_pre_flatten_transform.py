def _ext_pre_flatten_transform(
    tensor: torch.Tensor,
    fsdp_extension: Optional[FSDPExtensions] = None,
) -> tuple[torch.Tensor, Optional[Any]]:
    if fsdp_extension is not None:
        new_tensor, param_extension = fsdp_extension.pre_flatten_transform(tensor)
        if param_extension is not None:
            return new_tensor, param_extension
    return tensor, None
