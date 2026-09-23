def _clone_meta(
    input: TensorLikeType, *, memory_format: torch.memory_format = torch.preserve_format
) -> TensorLikeType:
    if memory_format != torch.preserve_format:
        return torch.empty(
            input.shape,
            dtype=input.dtype,
            layout=input.layout,
            device=input.device,
            memory_format=memory_format,
        )

    # memory_format == torch.preserve_format
    strides = utils.compute_elementwise_output_strides(input)
    return torch.empty_strided(
        input.shape,
        strides,
        dtype=input.dtype,
        layout=input.layout,
        device=input.device,
    )
