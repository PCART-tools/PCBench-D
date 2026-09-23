def make_functional_with_buffers(
    model: nn.Module, disable_autograd_tracking: bool = False
):
    warn_deprecated("make_functional_with_buffers", "torch.func.functional_call")
    return _nn_impl.make_functional_with_buffers(model, disable_autograd_tracking)
