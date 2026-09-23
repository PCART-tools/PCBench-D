def create_placeholder(
    name: str,
    dtype: torch.dtype,
    device: torch.device,
    size: Optional[list[int]] = None,
) -> TensorBox:
    """Creates a placeholder input buffers for producing subgraph_output."""
    input_buffer = InputBuffer(
        name=name,
        layout=FixedLayout(
            device,
            dtype,
            size if size else [],
            FlexibleLayout.contiguous_strides(size) if size else [],
        ),
    )
    return TensorBox.create(input_buffer)
