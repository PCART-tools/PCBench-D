def get_conv_mod_weight(mod: nn.Module) -> torch.Tensor:
    if (
        isinstance(mod, nn.Conv1d) or
        isinstance(mod, nn.Conv2d) or
        isinstance(mod, nn.Conv3d)
    ):
        return mod.weight.detach()
    elif (
        isinstance(mod, nni.ConvReLU1d) or
        isinstance(mod, nni.ConvReLU2d) or
        isinstance(mod, nni.ConvReLU3d)
    ):
        return mod[0].weight.detach()
    else:
        return mod._weight_bias()[0]  # type: ignore[operator]
