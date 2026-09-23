def get_equalization_qconfig_dict(
    layer_sqnr_dict: Dict[str, float],
    num_layers_to_equalize: int
) -> Any:
    """ Given the layer to SQNR dictionary, find the layers with the highest
    quantization errors, and return an equalization_qconfig_dict
    specifying to only equalize those top layers.

    Args:
        layer_sqnr_dict: Dictionary mapping layer names to SQNR values (found
            when comparing an equalized model against a float model)
        model_b: The equalized model used to construct the layer_sqnr_dict
        num_layers_to_equalize: Number of layers with the highest quantization
           errors to equalize
    """

    # Sort the layer_sqnr_dictionary values and get the layers with the lowest
    # SQNR values (aka highest quantization errors)
    layer_sqnr_sorted = sorted(layer_sqnr_dict.items(), key=lambda item: item[1])
    layers_to_equalize = layer_sqnr_sorted[:num_layers_to_equalize]

    # Constructs an equalization_qconfig_dict that specifies to only equalize
    # the layers with the highest quantization errors
    module_to_qconfig_list = list(
        map(lambda item: (item[0], default_equalization_qconfig), layers_to_equalize)
    )

    equalization_qconfig_dict = {"module_name": module_to_qconfig_list}
    return equalization_qconfig_dict
