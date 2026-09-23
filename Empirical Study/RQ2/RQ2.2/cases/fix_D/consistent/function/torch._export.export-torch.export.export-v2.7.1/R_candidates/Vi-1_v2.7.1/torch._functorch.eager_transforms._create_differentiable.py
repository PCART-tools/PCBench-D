def _create_differentiable(inps, level=None):
    def create_differentiable(x):
        if isinstance(x, torch.Tensor):
            with enable_inplace_requires_grad(True):
                return _set_tensor_requires_grad(x)
        raise ValueError(f"Thing passed to transform API must be Tensor, got {type(x)}")

    return tree_map(create_differentiable, inps)
