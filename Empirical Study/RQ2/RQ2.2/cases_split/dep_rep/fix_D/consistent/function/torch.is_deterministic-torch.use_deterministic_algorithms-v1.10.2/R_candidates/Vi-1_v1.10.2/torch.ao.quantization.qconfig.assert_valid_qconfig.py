def assert_valid_qconfig(qconfig: Optional[Union[QConfig, QConfigDynamic]],
                         mod: torch.nn.Module) -> None:
    if qconfig is None:
        return
    is_conv_transpose_mod = (
        isinstance(mod, torch.nn.ConvTranspose1d) or
        isinstance(mod, torch.nn.ConvTranspose2d) or
        isinstance(mod, torch.nn.ConvTranspose3d))
    if is_conv_transpose_mod:
        example_observer = qconfig.weight()
        is_per_channel = (
            isinstance(example_observer, torch.quantization.PerChannelMinMaxObserver) or
            isinstance(example_observer, torch.quantization.MovingAveragePerChannelMinMaxObserver)
        )
        assert not is_per_channel, \
            'Per channel weight observer is not supported yet for ConvTranspose{n}d.'
