def _verify_module(module: nn.Sequential) -> None:
    if not isinstance(module, nn.Sequential):
        raise TypeError("module must be nn.Sequential to be partitioned")

    named_children = list(module.named_children())
    if len(named_children) != len(module):
        raise ValueError("module with duplicate children is not supported")
