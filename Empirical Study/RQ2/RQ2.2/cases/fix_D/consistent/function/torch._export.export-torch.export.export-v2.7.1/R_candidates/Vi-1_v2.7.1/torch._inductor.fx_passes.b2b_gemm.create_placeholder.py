def create_placeholder(
    name: str, dtype: torch.dtype, device: torch.device
) -> TensorBox:
    """
    Creates a placeholder input buffers for producing subgraph_output
    """
    input_buffer = InputBuffer(name=name, layout=FixedLayout(device, dtype, [], []))
    return TensorBox.create(input_buffer)
