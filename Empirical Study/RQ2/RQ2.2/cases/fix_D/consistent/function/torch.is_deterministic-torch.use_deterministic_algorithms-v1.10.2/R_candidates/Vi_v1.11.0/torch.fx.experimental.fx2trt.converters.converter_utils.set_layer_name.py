def set_layer_name(layer: TRTLayer, target: Target, name: str) -> None:
    """
    Set the TensorRT layer name to "[TensorRT Layer Type]_[Original Op Name]_[FX Node Name with Suffix]"

    Args:
        layer (TRTLayer): A TensorRT layer of which we want to set the name.
        target (Target): A fx node.target. For call_function node, it's the function that
            the node represents.
        name (str): Consists of fx node.name with optional suffix.
    """
    target_name = target if isinstance(target, str) else f"acc_ops.{target.__name__}"
    layer.name = f"[{layer.type.name}]-[{target_name}]-[{name}]"
