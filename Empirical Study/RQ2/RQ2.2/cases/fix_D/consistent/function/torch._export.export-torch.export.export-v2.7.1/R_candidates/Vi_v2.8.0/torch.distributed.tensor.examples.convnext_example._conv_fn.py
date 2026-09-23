def _conv_fn(
    name: str,
    module: nn.Module,
    device_mesh: DeviceMesh,
) -> None:
    for name, param in module.named_parameters():
        dist_spec = [Replicate()]
        dist_param = torch.nn.Parameter(
            distribute_tensor(param, device_mesh, dist_spec)
        )
        dist_param.register_hook(lambda grad: grad.redistribute(placements=dist_spec))
        name = "_".join(name.split("."))
        module.register_parameter(name, dist_param)
