def _from_local_no_grad(
    local_tensor: torch.Tensor,
    sharding_spec: DTensorSpec,
) -> DTensor:
    """
    This method is similar to ``DTensor.from_local()`` except that in eager mode
    it avoids some CPU overhead by avoiding default args and not being differentiable.
    """

    if not compiled_autograd_enabled():
        return DTensor(
            # Use the local tensor directly instead of constructing a new tensor
            # variable, e.g. with `view_as()`, since this is not differentiable
            local_tensor,
            sharding_spec,
            requires_grad=local_tensor.requires_grad,
        )
    else:
        return DTensor.from_local(
            local_tensor,
            sharding_spec.mesh,
            sharding_spec.placements,
            shape=sharding_spec.shape,
            stride=sharding_spec.stride,
        )
