def from_dynamic_axes_to_dynamic_shapes(
    model,
    args: tuple[Any, ...],
    kwargs: dict[str, Any] | None,
    *,
    dynamic_axes=None,
    output_names: set[str],
    input_names: Sequence[str] | None = None,
) -> tuple[dict[str, Any | None] | None, tuple[Any, ...], dict[str, Any] | None]:
    """
    Converts dynamic_axes into dynamic_shapes by wrapping the axis names with ``torch.export.Dim.AUTO``.

    dynamic_axes examples:
    (1) dynamic_axes = {"x": {0: "my_custom_axis_name_1"}, "y": {1: "my_custom_axis_name_2"}}
    (2) dynamic_axes = {"x": [0], "y": [1]}

    these will be converted to dynamic_shapes respectively:
    (1) dynamic_shapes = {"x": {0: Dim.AUTO}, "y": {1: Dim.AUTO}}
    (2) dynamic_shapes = {"x": {0: Dim.AUTO}, "y": {1: Dim.AUTO}}

    Detail on Dim.AUTO: `#133620 <https://github.com/pytorch/pytorch/pull/133620>`_
    """
    # https://github.com/pytorch/pytorch/pull/128371
    # 1. The function does not need to provide dynamic_shapes to torch.export.export
    if dynamic_axes is None:
        return None, args, kwargs

    if input_names is None:
        input_names = []

    if kwargs is None:
        kwargs = {}

    dynamic_shapes: dict[str, Any | None] = {}
    for input_name, axes in dynamic_axes.items():
        # NOTE: torch.export.Dim.AUTO does its best to infer the min and max values
        # from the model, but it's not guaranteed to be dynamic.
        if input_name in output_names:
            # output names are not needed for dynamic_shapes
            continue
        if isinstance(axes, dict):
            if any(not isinstance(k, int) for k in axes.keys()):
                raise ValueError(
                    "The axis in dynamic_axes must be in the form of: dict[int, str] or list[int]."
                )
            dynamic_shapes[input_name] = {
                k: torch.export.Dim.AUTO  # type: ignore[attr-defined]
                for k, _ in axes.items()
            }
        elif isinstance(axes, list):
            if any(not isinstance(k, int) for k in axes):
                raise ValueError(
                    "The axis in dynamic_axes must be in the form of: dict[int, str] or list[int]."
                )
            dynamic_shapes[input_name] = {k: torch.export.Dim.AUTO for k in axes}  # type: ignore[attr-defined]
        elif axes is None:
            dynamic_shapes[input_name] = None
        else:
            raise ValueError(
                "Unsupported dynamic_axes format. Please provide a dict or a list."
            )

    for input_name in input_names:
        if input_name not in dynamic_shapes:
            dynamic_shapes[input_name] = None

    # Order the inputs according to the signature of the model
    sig = _signature(model)
    inputs = []
    for idx, param_name in enumerate(sig.parameters):
        if idx < len(args):
            inputs.append(args[idx])
        elif param_name in kwargs:
            inputs.append(kwargs[param_name])

    # We need tree structure to represent dynamic_shapes
    dynamic_shapes = _unflatten_dynamic_shapes_with_inputs_tree(inputs, dynamic_shapes)

    # Since the dynamic_shapes are now in the order of the model parameters,
    # we need to convert args and kwargs to the order of the model parameters.
    return dynamic_shapes, tuple(inputs), {}
