def _map_module_function_to_aten_operator_type():
    module_function_to_aten_operator: dict[Callable, torch._ops.OpOverloadPacket] = {}
    map_list = (
        ([torch.nn.Conv2d, F.conv1d], torch.ops.aten.conv1d.default),
        ([torch.nn.Conv2d, F.conv2d], torch.ops.aten.conv2d.default),
        ([torch.nn.Linear, F.linear], torch.ops.aten.linear.default),
        ([torch.nn.MaxPool2d, F.max_pool2d], torch.ops.aten.max_pool2d.default),
        (
            [
                torch.cat,
            ],
            torch.ops.aten.cat.default,
        ),
        ([torch.nn.AvgPool2d, F.avg_pool2d], torch.ops.aten.avg_pool2d.default),
        (
            [torch.nn.AdaptiveAvgPool2d, F.adaptive_avg_pool2d],
            torch.ops.aten.adaptive_avg_pool2d.default,
        ),
        (
            [
                torch.flatten,
            ],
            torch.ops.aten.flatten.using_ints,
        ),
        (
            [
                torch.matmul,
            ],
            torch.ops.aten.matmul.default,
        ),
    )
    for map_item in map_list:
        module_function_to_aten_operator.update(dict.fromkeys(map_item[0], map_item[1]))  # type: ignore[arg-type, call-overload]
    return module_function_to_aten_operator
