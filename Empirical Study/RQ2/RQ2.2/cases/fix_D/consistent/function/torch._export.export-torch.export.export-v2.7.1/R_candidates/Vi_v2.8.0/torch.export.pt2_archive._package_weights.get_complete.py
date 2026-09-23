def get_complete(
    group: OrderedSet[tuple[str, str]], models_weights: dict[str, Weights]
) -> tuple[str, str]:
    """
    `group` is a (model_name, weight_name) tuple.
    `model_weights` is a dictionary mapping from model name to its Weights.

    One of the tensor in `group` must be complete and they must share the
    same underlying storage.

    Returns the name of the complete tensor in the `group`. If multiple
    tensors are complete, returns an arbitrary one.
    """

    def get_tensor_properties(name_tuple: tuple[str, str]) -> TensorProperties:
        # returns the tensor properties
        (model_name, weight_name) = name_tuple
        return models_weights[model_name].get_weight_properties(weight_name)

    for name_tuple in group:
        tensor_property = get_tensor_properties(name_tuple)
        if tensor_property.is_complete():
            return name_tuple

    raise RuntimeError("No complete tensor found in the group!")
