@compatibility(is_backward_compatible=False)
def serialize_leaf_module(
    node: Node, weights_metadata: Dict, weights: Dict, name_prefix: str
) -> Dict:
    parameters: Dict[str, Any] = {}

    for p_name, p_value in node.attrs_for_lowering.items():  # type: ignore[attr-defined]
        if isinstance(p_value, torch.Tensor):
            weights_metadata.update(
                serialize_weight(p_value, weights, f"{name_prefix}.{p_name}")
            )
            weights[f"{name_prefix}.{p_name}"] = p_value
        else:
            parameters[p_name] = str(p_value)

    return parameters
