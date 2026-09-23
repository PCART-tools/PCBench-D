def update_qconfig_for_qat(
    qconfig_dict: Any,
    additional_qat_module_mapping: Dict[Callable, Callable]
) -> Any:
    """
    Update the qconfig_dict to account for module swaps during QAT.
    During QAT we perform a module swap on the nn.Module types to the corresponding nn.qat.modules types.
    """
    all_qat_mappings = get_combined_dict(
        get_default_qat_module_mappings(), additional_qat_module_mapping)
    object_type_dict = qconfig_dict.get("object_type", None)
    new_object_type_dict = object_type_dict.copy()
    for k, v in new_object_type_dict.items():
        if k in all_qat_mappings:
            object_type_dict[all_qat_mappings[k]] = v
    return qconfig_dict
