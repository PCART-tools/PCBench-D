def _adjust_scalar_from_onnx_to_fx(
    tensor: torch.Tensor,
    prim_value: Union[
        torch.Tensor,
        torch.SymInt,
        int,
        torch.SymFloat,
        float,
        torch.SymBool,
        bool,
    ],
) -> Union[
    torch.Tensor,
    int,
    float,
    bool,
]:
    """Helper function to wrap ORT-produced torch.Tensor as PyTorch variables"""
    assert isinstance(tensor, torch.Tensor), "ORT's output must be tensor."
    if isinstance(
        prim_value,
        (torch.SymInt, int, torch.SymFloat, float, torch.SymBool, bool),
    ):
        # Convert tensor back to scalar to match Dynamo's expectation.
        return tensor.item()
    return tensor
